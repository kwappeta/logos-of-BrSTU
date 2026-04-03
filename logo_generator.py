from PIL import Image, ImageDraw, ImageFont
import os

# Размер логотипа
LOGO_SIZE = 800

# Шрифты
def get_fonts():
    try:
        f_big = ImageFont.truetype("arial.ttf", 80)
        f_med = ImageFont.truetype("arial.ttf", 50)
        f_biggest = ImageFont.truetype("arial.ttf", 180)
        f_small = ImageFont.truetype("arial.ttf", 30) # Добавили, чтобы не было ошибки
        return f_big, f_med, f_biggest, f_small
    except:
        d = ImageFont.load_default()
        return d, d, d, d

font_big, font_medium, font_biggest, font_small = get_fonts()

def generate_logo(variant, additional_text=""):
    """Генерирует логотип: круглый (classic) или текстовый (text_only)"""
    
    # Создаем холст
    img = Image.new('RGB', (LOGO_SIZE, LOGO_SIZE), color='white')
    draw = ImageDraw.Draw(img)
    
    # Загрузка базового лого БрГТУ
    logo_base = None
    try:
        if os.path.exists("assets/logo.png"):
            logo_base = Image.open("assets/logo.png").convert("RGBA")
            logo_base = logo_base.resize((580, 580))
    except:
        pass

    # ВАРИАНТ 1: КЛАССИЧЕСКИЙ (КРУГЛЫЙ ЗНАЧОК)
    if variant == "classic":
        if logo_base:
            img.paste(logo_base, (110, 110), logo_base)
        else:
            draw.text((100, 300), "БрГТУ", fill="black", font=font_big)
            
        draw.text((140, 680), "БрГТУ", fill="blue", font=font_big)
        
        if additional_text:
            draw.text((140, 580), additional_text, fill="gray", font=font_medium)
    
    # ВАРИАНТ 2: ТОЛЬКО ТЕКСТ
    elif variant == "text_only":
        draw.text((80, 180), "БрГТУ", fill="blue", font=font_biggest)
        draw.text((80, 380), "Брестский государственный", fill="gray", font=font_medium)
        draw.text((80, 440), "технический университет", fill="gray", font=font_medium)
        
        if additional_text:
            draw.text((80, 500), additional_text, fill="gray", font=font_small)
    
    # Сохранение
    os.makedirs("output", exist_ok=True)
    
    if additional_text:
        safe_text = "".join([c for c in additional_text if c.isalnum() or c == ' ']).strip()
        filename = f"output/logo_{variant}_{safe_text.replace(' ', '_')}.png"
    else:
        filename = f"output/logo_{variant}.png"
    
    img.save(filename)
    return filename
