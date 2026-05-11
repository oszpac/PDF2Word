from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QTextEdit, QLabel
from PySide6.QtCore import Qt
from config import LOG_MAX_LINES


class ProgressPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._status_label = QLabel('进度：等待任务')
        self._status_label.setStyleSheet('color: #666; font-size: 12px;')
        layout.addWidget(self._status_label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(True)
        self._progress_bar.setStyleSheet('''
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
                height: 22px;
                background: #f0f0f0;
            }
            QProgressBar::chunk {
                background: #3370ff;
                border-radius: 3px;
            }
        ''')
        layout.addWidget(self._progress_bar)

        self._log_view = QTextEdit()
        self._log_view.setReadOnly(True)
        self._log_view.setMaximumHeight(120)
        self._log_view.setStyleSheet('''
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                background: #fafafa;
                font-size: 12px;
                color: #444;
            }
        ''')
        layout.addWidget(self._log_view)

    def update_progress(self, current, total, message):
        if total > 0:
            percent = int(current / total * 100)
            self._progress_bar.setValue(percent)
        self._status_label.setText(message)

    def append_log(self, message):
        self._log_view.append(message)
        if self._log_view.document().blockCount() > LOG_MAX_LINES:
            cursor = self._log_view.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.select(cursor.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

    def reset(self):
        self._progress_bar.setValue(0)
        self._status_label.setText('进度：等待任务')
        self._log_view.clear()
