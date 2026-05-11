from PySide6.QtCore import QThread, Signal

from models.pdf_model import PdfModel
from models.hybrid_engine import HybridEngine
from models.word_builder import WordBuilder
from utils.file_utils import get_output_path


class TaskRunner(QThread):
    progress_updated = Signal(int, int, str)
    log_message = Signal(str)
    task_finished = Signal(bool, str, str)

    def __init__(self, file_path, output_dir=None, output_path=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.output_dir = output_dir
        self.output_path = output_path
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        pdf_model = None
        try:
            pdf_model = PdfModel(self.file_path)
            pdf_model.load()

            info = pdf_model.get_file_info()
            self.log_message.emit(f'文件: {info["name"]}')
            self.log_message.emit(f'页数: {info["page_count"]}')
            self.log_message.emit(f'类型: {info["classification_label"]}')

            hybrid = HybridEngine(
                pdf_model,
                progress_callback=self._on_progress,
                log_callback=self.log_message.emit,
            )

            pages_data = hybrid.process()

            if self._is_cancelled:
                self.log_message.emit('任务已取消')
                self.task_finished.emit(False, '', '任务已取消')
                return

            builder = WordBuilder(
                pages_data,
                pdf_model,
                progress_callback=self._on_progress,
                log_callback=self.log_message.emit,
            )
            builder.build()

            if self._is_cancelled:
                self.log_message.emit('任务已取消')
                self.task_finished.emit(False, '', '任务已取消')
                return

            if self.output_path:
                output_path = self.output_path
            else:
                output_path = get_output_path(self.file_path, self.output_dir)
            builder.save(output_path)

            self.log_message.emit('转换完成！')
            self.task_finished.emit(True, output_path, '')
        except Exception as e:
            self.log_message.emit(f'错误: {str(e)}')
            self.task_finished.emit(False, '', str(e))
        finally:
            if pdf_model:
                pdf_model.close()

    def _on_progress(self, current, total, message):
        if not self._is_cancelled:
            self.progress_updated.emit(current, total, message)
