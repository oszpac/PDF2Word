from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage


class PreviewPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setStyleSheet('QScrollArea { border: none; background: #f0f0f0; }')

        self._preview_label = QLabel()
        self._preview_label.setAlignment(Qt.AlignCenter)
        self._preview_label.setText('选择PDF文件后可预览首页')
        self._preview_label.setStyleSheet('color: #999; font-size: 12px; padding: 20px;')
        self._preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._scroll_area.setWidget(self._preview_label)
        layout.addWidget(self._scroll_area)

    def show_preview(self, file_path):
        import fitz
        try:
            doc = fitz.open(file_path)
            if len(doc) > 0:
                page = doc[0]
                mat = fitz.Matrix(0.3, 0.3)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes('ppm')
                image = QImage.fromData(img_data)
                pixmap = QPixmap.fromImage(image)
                self._preview_label.setPixmap(pixmap)
                self._preview_label.setScaledContents(False)
            doc.close()
        except Exception:
            self._preview_label.setText('无法加载预览')
            self._preview_label.setStyleSheet('color: #999; font-size: 12px; padding: 20px;')

    def clear_preview(self):
        self._preview_label.setPixmap(QPixmap())
        self._preview_label.setText('选择PDF文件后可预览首页')
        self._preview_label.setStyleSheet('color: #999; font-size: 12px; padding: 20px;')
