import os

from models.pdf_model import PdfModel
from views.settings_dialog import SettingsDialog
from config import OCR_DPI, TEXT_DETECTION_THRESHOLD, DEFAULT_OUTPUT_DIR


class SettingsController:

    def __init__(self):
        self._output_dir = DEFAULT_OUTPUT_DIR
        self._ocr_dpi = OCR_DPI
        self._threshold = TEXT_DETECTION_THRESHOLD

    def open_settings(self, parent=None):
        dialog = SettingsDialog(parent)
        if dialog.exec():
            self._output_dir = dialog.get_output_dir()
            self._ocr_dpi = dialog.get_dpi()
            self._threshold = dialog.get_threshold()
            return True
        return False

    @property
    def output_dir(self):
        return self._output_dir

    @property
    def ocr_dpi(self):
        return self._ocr_dpi

    @property
    def threshold(self):
        return self._threshold

    def apply_threshold(self):
        import config
        config.TEXT_DETECTION_THRESHOLD = self._threshold

    def apply_dpi(self):
        import config
        config.OCR_DPI = self._ocr_dpi
