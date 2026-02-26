from PIL import Image, ImageDraw, ImageFont
import os

# Размер логотипа
LOGO_SIZE = 800

# Шрифты
try:
    font_big = ImageFont.truetype("arial.ttf", 80)
    font_medium = ImageFont.truetype("arial.ttf", 50)
    font_biggest = ImageFont.truetype("arial.ttf", 180)
except:
    font_big = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_biggest = ImageFont.load_default()

def generate_logo(variant, additional_text=""):
    """Генерирует логотип выбранного варианта"""
    
    img = Image.new('RGB', (LOGO_SIZE, LOGO_SIZE), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        logo_base = Image.open("assets/logo.png").convert("RGBA")
        logo_base = logo_base.resize((580, 580))
    except:
        logo_base = None
        draw.text((100, 300), "БрГТУ", fill="black", font=font_big)
    
    if variant == "classic":
        if logo_base:
            img.paste(logo_base, (110, 110), logo_base)
        draw.text((140, 680), "БрГТУ", fill="blue", font=font_big)
        
        # Добавляем дополнительный текст, если есть
        if additional_text:
            draw.text((140, 580), additional_text, fill="gray", font=font_medium)
    
    elif variant == "colored":
        bg_color = (0, 51, 160)  # тёмно-синий
        img = Image.new('RGB', (LOGO_SIZE, LOGO_SIZE), color=bg_color)
        draw = ImageDraw.Draw(img)
        if logo_base:
            img.paste(logo_base, (110, 110), logo_base)
        draw.text((140, 680), "БрГТУ", fill="white", font=font_big)
        
        if additional_text:
            draw.text((140, 580), additional_text, fill="white", font=font_medium)
    
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
