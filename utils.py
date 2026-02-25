from PIL import ImageFont
import os

# Константы размеров
BADGE_WIDTH, BADGE_HEIGHT = 1000, 640
LOGO_SIZE = 800

# Путь к шрифту (положи arial.ttf рядом или укажи системный)
FONT_PATH = "arial.ttf"  # или "C:/Windows/Fonts/arial.ttf"

# Глобальные шрифты
def load_fonts():
    try:
        big    = ImageFont.truetype(FONT_PATH, 80)
        medium = ImageFont.truetype(FONT_PATH, 50)
        small  = ImageFont.truetype(FONT_PATH, 40)
    except Exception:
        big    = ImageFont.load_default()
        medium = ImageFont.load_default()
        small  = ImageFont.load_default()
    return big, medium, small

FONT_BIG, FONT_MEDIUM, FONT_SMALL = load_fonts()


def get_output_path(filename):
    os.makedirs("output", exist_ok=True)
    return os.path.join("output", filename)
