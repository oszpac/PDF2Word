from docx.oxml.ns import qn
from config import FONT_CN_DEFAULT, FONT_CN_FALLBACK


CN_FONT_CANDIDATES = [FONT_CN_DEFAULT, FONT_CN_FALLBACK, '微软雅黑', '宋体', '黑体', '楷体', 'SimSun', 'SimHei', 'FangSong']


def set_cn_font(run, font_name=None, font_size=None):
    if font_name is None:
        font_name = FONT_CN_DEFAULT
    if font_size is not None:
        run.font.size = font_size
    run.font.name = font_name
    r = run._element.rPr
    if r is not None:
        rFonts = r.find(qn('w:rFonts'))
        if rFonts is None:
            from docx.oxml import OxmlElement
            rFonts = OxmlElement('w:rFonts')
            r.insert(0, rFonts)
        rFonts.set(qn('w:eastAsia'), font_name)
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)


def set_cell_font(cell, font_name=None, font_size=None):
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            set_cn_font(run, font_name, font_size)


def detect_available_cn_font():
    import subprocess
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             '[System.Drawing.Text.InstalledFontCollection]::new().Families | ForEach-Object { $_.Name }'],
            capture_output=True, text=True, timeout=10
        )
        installed = set(line.strip() for line in result.stdout.splitlines() if line.strip())
        for font in CN_FONT_CANDIDATES:
            if font in installed:
                return font
    except Exception:
        pass
    return FONT_CN_FALLBACK
