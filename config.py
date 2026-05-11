import os
import sys


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


TEXT_DETECTION_THRESHOLD = 50

OCR_DPI = 300

SUPPORTED_FORMATS = ['.pdf']

DEFAULT_OUTPUT_DIR = os.path.expanduser('~')

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 680
WINDOW_MIN_WIDTH = 720
WINDOW_MIN_HEIGHT = 500
WINDOW_TITLE = '智能PDF转Word'

FONT_CN_DEFAULT = '微软雅黑'
FONT_CN_FALLBACK = '宋体'
FONT_SIZE_DEFAULT = 11
FONT_SIZE_TITLE = 16
FONT_SIZE_HEADING = 14

PROGRESS_UPDATE_INTERVAL_MS = 100

LOG_MAX_LINES = 200

PADDLEOCR_MODEL_DIR = resource_path('inference')
