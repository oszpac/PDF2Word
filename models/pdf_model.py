import fitz
from config import TEXT_DETECTION_THRESHOLD


NATIVE = 'native'
SCANNED = 'scanned'
MIXED = 'mixed'


class PdfModel:

    def __init__(self, file_path):
        self.file_path = file_path
        self._doc = None
        self._page_count = 0
        self._classification = None
        self._page_classifications = []

    @property
    def doc(self):
        return self._doc

    @property
    def page_count(self):
        return self._page_count

    @property
    def classification(self):
        return self._classification

    @property
    def page_classifications(self):
        return self._page_classifications

    def load(self):
        self._doc = fitz.open(self.file_path)
        self._page_count = len(self._doc)
        self._classify()

    def close(self):
        if self._doc:
            self._doc.close()
            self._doc = None

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def _classify(self):
        sample_count = min(5, self._page_count)
        self._page_classifications = []
        native_count = 0

        for i in range(self._page_count):
            page = self._doc[i]
            text = page.get_text()
            char_count = len(text.strip())
            if char_count >= TEXT_DETECTION_THRESHOLD:
                self._page_classifications.append(NATIVE)
                native_count += 1
            else:
                self._page_classifications.append(SCANNED)

        if native_count == self._page_count:
            self._classification = NATIVE
        elif native_count == 0:
            self._classification = SCANNED
        else:
            self._classification = MIXED

    def is_page_native(self, page_index):
        if 0 <= page_index < len(self._page_classifications):
            return self._page_classifications[page_index] == NATIVE
        return False

    def get_file_info(self):
        import os
        size_bytes = os.path.getsize(self.file_path)
        return {
            'path': self.file_path,
            'name': os.path.basename(self.file_path),
            'size': size_bytes,
            'page_count': self._page_count,
            'classification': self._classification,
            'classification_label': self._get_classification_label(),
        }

    def _get_classification_label(self):
        labels = {NATIVE: '原生PDF（快速通道）', SCANNED: '扫描件PDF（OCR识别）',
                  MIXED: '混合PDF（自适应处理）'}
        return labels.get(self._classification, '未知')
