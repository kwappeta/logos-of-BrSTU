from PIL import Image, ImageDraw, ImageFont
import os

# Размеры бейджа
BADGE_WIDTH, BADGE_HEIGHT = 1000, 640

# Шрифты
try:
    font_big = ImageFont.truetype("arial.ttf", 70)
    font_medium = ImageFont.truetype("arial.ttf", 45)
    font_small = ImageFont.truetype("arial.ttf", 35)
except:
    font_big = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

def get_optimal_font_size(text, max_width, max_height, initial_font_size=70, min_font_size=14):
    """Каждое слово — на новой строке. Уменьшает шрифт, пока вся «стопка» не влезет в max_height."""
    font_size = initial_font_size
    
    # Разбиваем текст на список слов, убираем пустые строки
    words = text.split()
    lines = [word for word in words if word.strip()]  # убираем пустые, если ввели два пробела
    
    if not lines:
        return initial_font_size, []

    while font_size >= min_font_size:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        total_height = 0
        fits_width = True
        
        for line in lines:
            # Временное изображение для измерения
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            
            # Проверяем, влезет ли слово по ширине
            if text_width > max_width:
                fits_width = False
                break
            total_height += line_height + 8  # 8 - межстрочный интервал
        
        # Если все слова влезают и по ширине, и по высоте — готово
        if fits_width and total_height <= max_height:
            return font_size, lines
        
        font_size -= 5
    
    # Если ничего не подошло, возвращаем минимальный размер
    return min_font_size, lines

def generate_badge(full_name, position):
    """Генерирует бейдж с контролем границ"""
    
    # ОГРАНИЧЕНИЕ: берем только первые 20 символов для ФИО
    full_name = full_name[:20]
    position = position[:30] if position else ""
    
    # Создаём белый фон
    img = Image.new('RGB', (BADGE_WIDTH, BADGE_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    
    # 1. Логотип
    try:
        logo = Image.open("assets/logo.png").convert("RGBA")
        logo = logo.resize((300, 300))
        img.paste(logo, (70, 170), logo)
    except:
        draw.text((80, 200), "[ЛОГОТИП]", fill="black", font=font_medium)

    # Константы для текста
    TEXT_X = 420
    MAX_TEXT_WIDTH = BADGE_WIDTH - TEXT_X - 60
    
    # 2. Отрисовка ФИО (каждое слово с новой строки)
    name_font_size, name_lines = get_optimal_font_size(full_name.upper(), MAX_TEXT_WIDTH, 250, 70, 16)
    try:
        name_font = ImageFont.truetype("arial.ttf", name_font_size)
    except:
        name_font = font_big

    current_y = 120
    for line in name_lines:
        draw.text((TEXT_X, current_y), line, fill="black", font=name_font)
        bbox = draw.textbbox((TEXT_X, current_y), line, font=name_font)
        current_y += (bbox[3] - bbox[1]) + 10

    # 3. Отрисовка Должности (каждое слово с новой строки)
    if position:
        # Вычисляем остаток высоты до подписи БрГТУ
        rem_height = (BADGE_HEIGHT - 100) - current_y
        pos_font_size, pos_lines = get_optimal_font_size(position, MAX_TEXT_WIDTH, rem_height, 40, 12)
        
        try:
            pos_font = ImageFont.truetype("arial.ttf", pos_font_size)
        except:
            pos_font = font_medium

        current_y += 15
        for line in pos_lines:
            # Проверка на вылет за нижнюю границу
            bbox = draw.textbbox((TEXT_X, current_y), line, font=pos_font)
            line_height = bbox[3] - bbox[1]
            
            if current_y + line_height > BADGE_HEIGHT - 80:
                # Если строка не помещается, обрезаем
                if len(line) > 5:
                    draw.text((TEXT_X, current_y), line[:15] + "...", fill="gray", font=font_small)
                break
                
            draw.text((TEXT_X, current_y), line, fill="gray", font=pos_font)
            current_y += line_height + 8

    # 4. Подпись БрГТУ (всегда снизу)
    draw.text((TEXT_X, BADGE_HEIGHT - 80), "БрГТУ", fill="blue", font=font_small)
    
    # 5. Рамка
    draw.rectangle([(20, 20), (BADGE_WIDTH-20, BADGE_HEIGHT-20)], outline="blue", width=8)
    
    # Сохранение
    os.makedirs("output", exist_ok=True)
    
    # Безопасное имя файла
    safe_name = "".join([c for c in full_name if c.isalnum() or c == ' ']).strip()
    if safe_name:
        filename = f"output/badge_{safe_name[:15].replace(' ', '_')}.png"
    else:
        filename = f"output/badge_result.png"
    
    img.save(filename)
    return filename
