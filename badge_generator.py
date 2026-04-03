from PIL import Image, ImageDraw, ImageFont
import os

# Размеры бейджа
BADGE_WIDTH, BADGE_HEIGHT = 1000, 640

def get_optimal_font_size(text, max_width, max_height, initial_font_size=72, min_font_size=18):
    """Разбивает текст по словам и подбирает размер шрифта"""
    words = [word for word in text.split() if word.strip()]
    if not words:
        return initial_font_size, []

    font_size = initial_font_size
    while font_size >= min_font_size:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        total_height = 0
        fits = True

        for word in words:
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), word, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if text_width > max_width:
                fits = False
                break
            total_height += text_height + 10  # межстрочный интервал

        if fits and total_height <= max_height:
            return font_size, words
        
        font_size -= 5

    return min_font_size, words

def generate_badge(full_name: str, position: str, color: str = "#0056b3"):
    """
    Генерирует 2D бейдж БрГТУ
    """
    # Ограничение длины
    full_name = full_name.strip()[:30]
    position = position.strip()[:45] if position else ""

    # Создание изображения
    img = Image.new('RGB', (BADGE_WIDTH, BADGE_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    try:
        logo = Image.open("assets/logo.png").convert("RGBA")
        logo = logo.resize((300, 300))
        img.paste(logo, (70, 170), logo)
    except FileNotFoundError:
        draw.text((80, 200), "[ЛОГОТИП]", fill="black", font=ImageFont.truetype("arial.ttf", 40))
    except Exception:
        pass

    TEXT_X = 420
    MAX_TEXT_WIDTH = BADGE_WIDTH - TEXT_X - 70
    name_font_size, name_lines = get_optimal_font_size(full_name.upper(), MAX_TEXT_WIDTH, 260, 72, 20)
    try:
        name_font = ImageFont.truetype("arial.ttf", name_font_size)
    except:
        name_font = ImageFont.load_default()

    current_y = 130
    for line in name_lines:
        draw.text((TEXT_X, current_y), line, fill="black", font=name_font)
        bbox = draw.textbbox((TEXT_X, current_y), line, font=name_font)
        current_y += (bbox[3] - bbox[1]) + 12
    if position:
        rem_height = BADGE_HEIGHT - current_y - 110
        pos_font_size, pos_lines = get_optimal_font_size(position, MAX_TEXT_WIDTH, rem_height, 42, 16)
        
        try:
            pos_font = ImageFont.truetype("arial.ttf", pos_font_size)
        except:
            pos_font = ImageFont.load_default()

        current_y += 25
        for line in pos_lines:
            bbox = draw.textbbox((TEXT_X, current_y), line, font=pos_font)
            line_height = bbox[3] - bbox[1]
            
            if current_y + line_height > BADGE_HEIGHT - 95:
                break
                
            draw.text((TEXT_X, current_y), line, fill="gray", font=pos_font)
            current_y += line_height + 8
    try:
        brgtu_font = ImageFont.truetype("arial.ttf", 42)
    except:
        brgtu_font = ImageFont.load_default()
    
    draw.text((TEXT_X, BADGE_HEIGHT - 82), "БрГТУ", fill=color, font=brgtu_font)
    draw.rectangle([(20, 20), (BADGE_WIDTH - 20, BADGE_HEIGHT - 20)], 
                   outline=color, width=10)
    os.makedirs("output", exist_ok=True)
    
    safe_name = "".join(c for c in full_name if c.isalnum() or c == " ").strip()
    if safe_name:
        filename = f"output/badge_{safe_name[:20].replace(' ', '_')}.png"
    else:
        filename = "output/badge_result.png"
    img.save(filename)
    return filename
