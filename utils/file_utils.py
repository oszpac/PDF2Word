import os
from config import SUPPORTED_FORMATS


def validate_pdf_file(file_path):
    if not os.path.isfile(file_path):
        return False, '文件不存在'

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        return False, f'不支持的文件格式: {ext}，仅支持 {", ".join(SUPPORTED_FORMATS)}'

    try:
        size = os.path.getsize(file_path)
        if size == 0:
            return False, '文件为空，无法处理'
    except OSError:
        return False, '无法读取文件信息'

    return True, ''


def get_output_path(input_pdf_path, output_dir=None):
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    if output_dir is None:
        from config import DEFAULT_OUTPUT_DIR
        output_dir = DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{base_name}_转换结果.docx')
    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(output_dir, f'{base_name}_转换结果({counter}).docx')
        counter += 1
    return output_path


def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f'{size_bytes} B'
    elif size_bytes < 1024 * 1024:
        return f'{size_bytes / 1024:.1f} KB'
    else:
        return f'{size_bytes / (1024 * 1024):.1f} MB'
