from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class DropArea(QWidget):
    file_dropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_file = None
        self._init_ui()

    def _init_ui(self):
        self.setAcceptDrops(True)
        self.setMinimumHeight(160)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self._placeholder = QLabel()
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._placeholder.setStyleSheet('''
            QLabel {
                color: #888;
                font-size: 14px;
                border: 2px dashed #bbb;
                border-radius: 12px;
                padding: 40px 20px;
                background-color: #fafafa;
            }
        ''')
        self._placeholder.setText('拖拽PDF文件到此处\n或点击选择文件')
        layout.addWidget(self._placeholder)

        self._file_label = QLabel()
        self._file_label.setAlignment(Qt.AlignCenter)
        self._file_label.setStyleSheet('''
            QLabel {
                color: #333;
                font-size: 13px;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 12px 20px;
                background-color: #f0f7ff;
            }
        ''')
        self._file_label.hide()
        layout.addWidget(self._file_label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.pdf'):
                    event.acceptProposedAction()
                    self._placeholder.setStyleSheet('''
                        QLabel {
                            color: #3370ff;
                            font-size: 14px;
                            border: 2px dashed #3370ff;
                            border-radius: 12px;
                            padding: 40px 20px;
                            background-color: #eef3ff;
                        }
                    ''')
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self._reset_style()

    def dropEvent(self, event: QDropEvent):
        self._reset_style()
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith('.pdf'):
                    self._selected_file = file_path
                    self._show_selected_file(file_path)
                    self.file_dropped.emit(file_path)
                    return

    def mousePressEvent(self, event):
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择PDF文件', '', 'PDF文件 (*.pdf)'
        )
        if file_path:
            self._selected_file = file_path
            self._show_selected_file(file_path)
            self.file_dropped.emit(file_path)

    def _show_selected_file(self, file_path):
        import os
        self._placeholder.hide()
        self._file_label.setText(os.path.basename(file_path))
        self._file_label.show()
        self.setMinimumHeight(60)

    def _reset_style(self):
        self._placeholder.setStyleSheet('''
            QLabel {
                color: #888;
                font-size: 14px;
                border: 2px dashed #bbb;
                border-radius: 12px;
                padding: 40px 20px;
                background-color: #fafafa;
            }
        ''')

    def reset(self):
        self._selected_file = None
        self._file_label.hide()
        self._placeholder.show()
        self.setMinimumHeight(160)
        self._reset_style()

    @property
    def selected_file(self):
        return self._selected_file
