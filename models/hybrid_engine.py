from models.pdf_model import NATIVE, SCANNED, MIXED
from models.extract_engine import ExtractEngine
from models.ocr_engine import OcrEngine


class HybridEngine:

    def __init__(self, pdf_model, progress_callback=None, log_callback=None):
        self.pdf_model = pdf_model
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def process(self):
        classification = self.pdf_model.classification
        self._log(f'PDF分类结果: {self.pdf_model.get_file_info()["classification_label"]}')
        self._log(f'总页数: {self.pdf_model.page_count}')

        if classification == NATIVE:
            self._log('启动原生提取通道（模式A）')
            return self._process_native()
        elif classification == SCANNED:
            self._log('启动OCR识别通道（模式B）')
            return self._process_scanned()
        else:
            self._log('启动自适应混合通道（模式C）')
            return self._process_mixed()

    def _process_native(self):
        engine = ExtractEngine(self.pdf_model, progress_callback=self.progress_callback)
        return engine.extract_all()

    def _process_scanned(self):
        engine = OcrEngine(self.pdf_model, progress_callback=self.progress_callback)
        return engine.extract_all()

    def _process_mixed(self):
        extract_engine = ExtractEngine(self.pdf_model, progress_callback=self.progress_callback)
        ocr_engine = OcrEngine(self.pdf_model, progress_callback=self.progress_callback)
        pages_data = []

        for i in range(self.pdf_model.page_count):
            is_native = self.pdf_model.is_page_native(i)
            mode_label = '原生通道' if is_native else 'OCR通道'
            self._log(f'第 {i + 1}/{self.pdf_model.page_count} 页 -> {mode_label}')

            if is_native:
                page_data = extract_engine.extract_page(i)
            else:
                page_data = ocr_engine.extract_page(i)

            pages_data.append(page_data)

        return pages_data

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)
