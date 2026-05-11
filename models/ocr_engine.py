import tempfile
import os
import fitz
from PIL import Image
from config import OCR_DPI


class OcrEngine:

    def __init__(self, pdf_model, progress_callback=None):
        self.pdf_model = pdf_model
        self.progress_callback = progress_callback
        self._ocr = None
        self._ocr_available = None

    @property
    def ocr_available(self):
        if self._ocr_available is None:
            try:
                from paddleocr import PaddleOCR
                self._ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
                self._ocr_available = True
            except Exception:
                self._ocr_available = False
        return self._ocr_available

    def extract_all(self):
        pages_data = []
        total = self.pdf_model.page_count
        for i in range(total):
            if self.progress_callback:
                self.progress_callback(i + 1, total, f'正在进行OCR识别第 {i + 1}/{total} 页')
            page_data = self.extract_page(i)
            pages_data.append(page_data)
        return pages_data

    def extract_page(self, page_index):
        if not self.ocr_available:
            raise RuntimeError('PaddleOCR 不可用，请确认已正确安装 paddleocr 及 paddlepaddle')

        if self.progress_callback:
            self.progress_callback(page_index + 1, self.pdf_model.page_count,
                                   f'正在进行OCR识别第 {page_index + 1}/{self.pdf_model.page_count} 页')

        img_path = self._page_to_image(page_index)

        try:
            ocr_result = self._ocr.ocr(img_path, cls=True)
        finally:
            self._cleanup_image(img_path)

        blocks = self._parse_ocr_result(ocr_result, page_index)
        return {'page_index': page_index, 'blocks': blocks}

    def _page_to_image(self, page_index):
        page = self.pdf_model.doc[page_index]
        mat = fitz.Matrix(OCR_DPI / 72, OCR_DPI / 72)
        pix = page.get_pixmap(matrix=mat)
        fd, img_path = tempfile.mkstemp(suffix='.png', prefix='pdf2word_ocr_')
        os.close(fd)
        pix.save(img_path)
        return img_path

    def _cleanup_image(self, img_path):
        try:
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception:
            pass

    def _parse_ocr_result(self, ocr_result, page_index):
        blocks = []
        scale = 72.0 / OCR_DPI

        if ocr_result is None or (isinstance(ocr_result, list) and len(ocr_result) == 0):
            return blocks

        result_list = ocr_result[0] if isinstance(ocr_result, list) and len(ocr_result) > 0 else ocr_result

        if result_list is None:
            return blocks

        for item in result_list:
            if item is None:
                continue
            bbox_points = item[0]
            text = item[1][0] if isinstance(item[1], (list, tuple)) else item[1]
            confidence = item[1][1] if isinstance(item[1], (list, tuple)) and len(item[1]) > 1 else 0.0

            if not text.strip():
                continue

            x1 = min(p[0] for p in bbox_points) * scale
            y1 = min(p[1] for p in bbox_points) * scale
            x2 = max(p[0] for p in bbox_points) * scale
            y2 = max(p[1] for p in bbox_points) * scale

            blocks.append({
                'type': 'text',
                'text': text.strip(),
                'spans': [{'text': text.strip(), 'font': '', 'size': 11,
                           'color': 0, 'flags': 0, 'bbox': (x1, y1, x2, y2)}],
                'bbox': (x1, y1, x2, y2),
                'x': x1,
                'y': y1,
                'width': x2 - x1,
                'height': y2 - y1,
                'confidence': confidence,
            })

        blocks.sort(key=lambda b: (b['y'], b['x']))
        return blocks
