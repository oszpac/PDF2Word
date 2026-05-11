import os

from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import QObject

from models.pdf_model import PdfModel
from models.task_runner import TaskRunner
from utils.file_utils import validate_pdf_file
from controllers.settings_controller import SettingsController
from views.main_window import MainWindow


class AppController(QObject):

    def __init__(self):
        super().__init__()
        self._current_file = None
        self._task_runner = None
        self._settings_controller = SettingsController()

        self._window = MainWindow(controller=self)
        self._connect_signals()

    def _connect_signals(self):
        self._window.file_selected.connect(self._on_file_selected)
        self._window.convert_clicked.connect(self._on_convert)
        self._window.cancel_clicked.connect(self._on_cancel)
        self._window.preview_clicked.connect(self._on_preview)

    def show(self):
        self._window.show()

    def open_settings(self):
        self._settings_controller.open_settings(self._window)

    def _on_file_selected(self, file_path):
        valid, error_msg = validate_pdf_file(file_path)
        if not valid:
            QMessageBox.warning(self._window, '文件错误', error_msg)
            return

        try:
            pdf_model = PdfModel(file_path)
            pdf_model.load()
            info = pdf_model.get_file_info()
            pdf_model.close()

            self._current_file = file_path
            self._window.show_file_info(info)
            self._window.append_log(f'已加载: {info["name"]}')
            self._window.append_log(f'分类: {info["classification_label"]}')
        except Exception as e:
            QMessageBox.critical(self._window, '加载失败', f'无法打开PDF文件：{str(e)}')

    def _on_convert(self):
        if not self._current_file:
            return

        base_name = os.path.splitext(os.path.basename(self._current_file))[0]
        default_dir = self._settings_controller.output_dir
        default_path = os.path.join(default_dir, f'{base_name}_转换结果.docx')

        output_path, _ = QFileDialog.getSaveFileName(
            self._window,
            '保存Word文档',
            default_path,
            'Word文档 (*.docx)',
        )
        if not output_path:
            return

        self._settings_controller.apply_threshold()
        self._settings_controller.apply_dpi()

        self._window.set_processing_state(True)
        self._window.progress_panel.reset()
        self._window.append_log(f'输出路径: {output_path}')
        self._window.append_log('开始转换任务...')

        self._task_runner = TaskRunner(
            self._current_file,
            output_dir=self._settings_controller.output_dir,
            output_path=output_path,
        )
        self._task_runner.progress_updated.connect(self._window.update_progress)
        self._task_runner.log_message.connect(self._window.append_log)
        self._task_runner.task_finished.connect(self._on_task_finished)
        self._task_runner.start()

    def _on_cancel(self):
        if self._task_runner and self._task_runner.isRunning():
            self._task_runner.cancel()
            self._window.append_log('正在取消任务...')
            self._window.set_processing_state(False)

    def _on_preview(self):
        QMessageBox.information(
            self._window, '预览',
            f'当前文件: {os.path.basename(self._current_file or "")}\n'
            '可使用系统关联的PDF阅读器打开预览。'
        )

    def _on_task_finished(self, success, output_path, error_msg):
        self._window.set_processing_state(False)
        self._task_runner = None

        if success:
            self._window.append_log(f'✓ 转换成功！')
            self._window.append_log(f'保存位置: {output_path}')
            self._window.show_saved_path(output_path)
            result = QMessageBox.question(
                self._window,
                '转换完成',
                f'文档已保存到：\n{output_path}\n\n是否打开文件？',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if result == QMessageBox.Yes:
                os.startfile(output_path)
        else:
            if error_msg != '任务已取消':
                QMessageBox.critical(self._window, '转换失败', f'转换过程中发生错误：\n{error_msg}')
