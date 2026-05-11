from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QSplitter, QStatusBar, QMenuBar, QMenu, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont

from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, WINDOW_TITLE
from views.drop_area import DropArea
from views.progress_panel import ProgressPanel
from views.preview_panel import PreviewPanel
from views.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    file_selected = Signal(str)
    convert_clicked = Signal()
    cancel_clicked = Signal()
    preview_clicked = Signal()

    def __init__(self, controller=None):
        super().__init__()
        self._controller = controller
        self._last_saved_path = ''
        self._init_window()
        self._init_ui()
        self._init_menu()

    def _init_window(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet('''
            QMainWindow {
                background-color: #ffffff;
            }
        ''')

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(16)

        self._drop_area = DropArea()
        self._drop_area.file_dropped.connect(self.file_selected.emit)
        main_layout.addWidget(self._drop_area)

        self._info_frame = QFrame()
        self._info_frame.setStyleSheet('''
            QFrame {
                background: #f7f8fa;
                border-radius: 8px;
                padding: 12px;
            }
        ''')
        info_layout = QHBoxLayout(self._info_frame)
        info_layout.setContentsMargins(12, 10, 12, 10)

        left_info = QVBoxLayout()
        self._file_name_label = QLabel('尚未选择文件')
        self._file_name_label.setFont(QFont('微软雅黑', 11, QFont.Bold))
        self._file_name_label.setStyleSheet('color: #333;')
        left_info.addWidget(self._file_name_label)

        self._file_detail_label = QLabel('')
        self._file_detail_label.setStyleSheet('color: #888; font-size: 12px;')
        left_info.addWidget(self._file_detail_label)

        info_layout.addLayout(left_info)
        info_layout.addStretch()

        right_info = QVBoxLayout()
        right_info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._mode_label = QLabel('')
        self._mode_label.setStyleSheet('color: #3370ff; font-size: 12px; font-weight: bold;')
        right_info.addWidget(self._mode_label)
        info_layout.addLayout(right_info)

        self._info_frame.hide()
        main_layout.addWidget(self._info_frame)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self._convert_btn = QPushButton('▶  开始转换')
        self._convert_btn.setMinimumHeight(40)
        self._convert_btn.setStyleSheet('''
            QPushButton {
                background-color: #3370ff;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 28px;
            }
            QPushButton:hover {
                background-color: #2860e0;
            }
            QPushButton:pressed {
                background-color: #1e50c0;
            }
            QPushButton:disabled {
                background-color: #b0c8ff;
            }
        ''')
        self._convert_btn.clicked.connect(self.convert_clicked.emit)
        self._convert_btn.setEnabled(False)
        btn_layout.addWidget(self._convert_btn)

        self._cancel_btn = QPushButton('取消')
        self._cancel_btn.setMinimumHeight(40)
        self._cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #f0f0f0;
                color: #666;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 13px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #e5e5e5;
            }
            QPushButton:disabled {
                color: #ccc;
            }
        ''')
        self._cancel_btn.clicked.connect(self.cancel_clicked.emit)
        self._cancel_btn.setEnabled(False)
        btn_layout.addWidget(self._cancel_btn)

        btn_layout.addStretch()

        self._preview_btn = QPushButton('🔍 预览PDF')
        self._preview_btn.setMinimumHeight(40)
        self._preview_btn.setStyleSheet('''
            QPushButton {
                background-color: #ffffff;
                color: #555;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 13px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
            }
            QPushButton:disabled {
                color: #ccc;
            }
        ''')
        self._preview_btn.clicked.connect(self.preview_clicked.emit)
        self._preview_btn.setEnabled(False)
        btn_layout.addWidget(self._preview_btn)

        main_layout.addLayout(btn_layout)

        self._progress_panel = ProgressPanel()
        main_layout.addWidget(self._progress_panel)

        self._saved_frame = QFrame()
        self._saved_frame.setStyleSheet('''
            QFrame {
                background: #f0f7ff;
                border: 1px solid #b8d4ff;
                border-radius: 8px;
                padding: 8px;
            }
        ''')
        saved_layout = QHBoxLayout(self._saved_frame)
        saved_layout.setContentsMargins(12, 8, 12, 8)

        self._saved_icon = QLabel('📄')
        self._saved_icon.setFixedWidth(24)
        saved_layout.addWidget(self._saved_icon)

        self._saved_path_label = QLabel('')
        self._saved_path_label.setStyleSheet('color: #3370ff; font-size: 12px; border: none; background: transparent;')
        self._saved_path_label.setWordWrap(True)
        self._saved_path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        saved_layout.addWidget(self._saved_path_label)

        self._open_folder_btn = QPushButton('📂 打开文件夹')
        self._open_folder_btn.setFixedWidth(110)
        self._open_folder_btn.setStyleSheet('''
            QPushButton {
                background-color: #3370ff;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #2860e0;
            }
        ''')
        self._open_folder_btn.clicked.connect(self._open_saved_folder)
        saved_layout.addWidget(self._open_folder_btn)

        self._saved_frame.hide()
        main_layout.addWidget(self._saved_frame)

        main_layout.addStretch()

        self._status_bar = QStatusBar()
        self._status_bar.setStyleSheet('QStatusBar { color: #888; font-size: 11px; }')
        self._status_bar.showMessage('就绪')
        self.setStatusBar(self._status_bar)

    def _init_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('文件(&F)')
        open_action = QAction('打开PDF...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self._drop_area.mousePressEvent)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        tools_menu = menu_bar.addMenu('工具(&T)')
        settings_action = QAction('设置...', self)
        settings_action.triggered.connect(self._open_settings)
        tools_menu.addAction(settings_action)

    def _open_settings(self):
        if self._controller:
            self._controller.open_settings()

    def show_file_info(self, info):
        self._file_name_label.setText(info['name'])
        self._file_detail_label.setText(
            f"共 {info['page_count']} 页  |  {info['classification_label']}"
        )
        self._mode_label.setText(info['classification_label'])
        self._info_frame.show()
        self._convert_btn.setEnabled(True)
        self._preview_btn.setEnabled(True)

    def clear_file_info(self):
        self._file_name_label.setText('尚未选择文件')
        self._file_detail_label.setText('')
        self._mode_label.setText('')
        self._info_frame.hide()
        self._convert_btn.setEnabled(False)
        self._preview_btn.setEnabled(False)
        self._saved_frame.hide()
        self._saved_path_label.setText('')
        self._last_saved_path = ''

    def set_processing_state(self, processing):
        self._convert_btn.setEnabled(not processing)
        self._cancel_btn.setEnabled(processing)
        self._drop_area.setAcceptDrops(not processing)
        if processing:
            self._status_bar.showMessage('正在转换...')
        else:
            self._status_bar.showMessage('就绪')

    def update_progress(self, current, total, message):
        self._progress_panel.update_progress(current, total, message)

    def append_log(self, message):
        self._progress_panel.append_log(message)

    def reset(self):
        self._progress_panel.reset()
        self.clear_file_info()
        self._drop_area.reset()
        self._saved_frame.hide()
        self._saved_path_label.setText('')
        self._last_saved_path = ''

    def show_saved_path(self, path):
        self._last_saved_path = path
        self._saved_path_label.setText(path)
        self._saved_frame.show()

    def _open_saved_folder(self):
        import os
        if self._last_saved_path and os.path.isfile(self._last_saved_path):
            os.startfile(os.path.dirname(self._last_saved_path))

    @property
    def progress_panel(self):
        return self._progress_panel

    @property
    def drop_area(self):
        return self._drop_area
