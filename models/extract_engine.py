import fitz
from config import FONT_SIZE_DEFAULT


class ExtractEngine:

    def __init__(self, pdf_model, progress_callback=None):
        self.pdf_model = pdf_model
        self.progress_callback = progress_callback

    def extract_all(self):
        pages_data = []
        total = self.pdf_model.page_count
        for i in range(total):
            if self.progress_callback:
                self.progress_callback(i + 1, total, f'正在提取第 {i + 1}/{total} 页（原生通道）')
            page = self.pdf_model.doc[i]
            blocks = self._extract_page(page, i)
            pages_data.append({'page_index': i, 'blocks': blocks})
        return pages_data

    def extract_page(self, page_index):
        if self.progress_callback:
            self.progress_callback(page_index + 1, self.pdf_model.page_count,
                                   f'正在提取第 {page_index + 1} 页（原生通道）')
        page = self.pdf_model.doc[page_index]
        blocks = self._extract_page(page, page_index)
        return {'page_index': page_index, 'blocks': blocks}

    def _extract_page(self, page, page_index):
        text_blocks = []
        try:
            blocks = page.get_text('dict', flags=fitz.TEXT_PRESERVE_WHITESPACE)['blocks']
        except Exception:
            blocks = page.get_text('dict')['blocks']

        for block in blocks:
            if block['type'] == 0:
                for line in block['lines']:
                    line_text = ''
                    spans_data = []
                    for span in line['spans']:
                        spans_data.append({
                            'text': span['text'],
                            'font': span.get('font', ''),
                            'size': span.get('size', FONT_SIZE_DEFAULT),
                            'color': span.get('color', 0),
                            'flags': span.get('flags', 0),
                            'bbox': span['bbox'],
                        })
                        line_text += span['text']

                    if line_text.strip():
                        bbox = line['bbox']
                        text_blocks.append({
                            'type': 'text',
                            'text': line_text.strip(),
                            'spans': spans_data,
                            'bbox': bbox,
                            'x': bbox[0],
                            'y': bbox[1],
                            'width': bbox[2] - bbox[0],
                            'height': bbox[3] - bbox[1],
                            'block_bbox': block['bbox'],
                        })

            elif block['type'] == 1:
                bbox = block['bbox']
                text_blocks.append({
                    'type': 'image',
                    'bbox': bbox,
                    'x': bbox[0],
                    'y': bbox[1],
                    'width': bbox[2] - bbox[0],
                    'height': bbox[3] - bbox[1],
                    'image_index': block.get('image', -1),
                })

        text_blocks.sort(key=lambda b: (b['y'], b['x']))
        return text_blocks
