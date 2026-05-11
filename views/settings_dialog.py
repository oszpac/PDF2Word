from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QFileDialog, QDialogButtonBox
)
from config import OCR_DPI, TEXT_DETECTION_THRESHOLD, DEFAULT_OUTPUT_DIR


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_output_dir = DEFAULT_OUTPUT_DIR
        self._current_dpi = OCR_DPI
        self._current_threshold = TEXT_DETECTION_THRESHOLD
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle('设置')
        self.setMinimumWidth(480)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel('默认输出目录：'))
        self._dir_edit = QLineEdit(self._current_output_dir)
        self._dir_edit.setReadOnly(True)
        dir_layout.addWidget(self._dir_edit)
        browse_btn = QPushButton('浏览...')
        browse_btn.clicked.connect(self._browse_output_dir)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)

        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(QLabel('OCR转换DPI：'))
        self._dpi_spin = QSpinBox()
        self._dpi_spin.setRange(72, 600)
        self._dpi_spin.setValue(self._current_dpi)
        self._dpi_spin.setSuffix(' DPI')
        dpi_layout.addWidget(self._dpi_spin)
        dpi_layout.addStretch()
        layout.addLayout(dpi_layout)

        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel('文本检测阈值：'))
        self._threshold_spin = QSpinBox()
        self._threshold_spin.setRange(10, 500)
        self._threshold_spin.setValue(self._current_threshold)
        self._threshold_spin.setSuffix(' 字符')
        threshold_layout.addWidget(self._threshold_spin)
        threshold_layout.addStretch()
        layout.addLayout(threshold_layout)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _browse_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, '选择输出目录', self._dir_edit.text())
        if directory:
            self._dir_edit.setText(directory)

    def _on_accept(self):
        self._current_output_dir = self._dir_edit.text()
        self._current_dpi = self._dpi_spin.value()
        self._current_threshold = self._threshold_spin.value()
        self.accept()

    def get_output_dir(self):
        return self._current_output_dir

    def get_dpi(self):
        return self._current_dpi

    def get_threshold(self):
        return self._current_threshold
