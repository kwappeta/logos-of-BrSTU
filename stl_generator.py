import numpy as np
from PIL import Image, ImageDraw, ImageFont
from stl import mesh
import os
def load_font(size, font_name="arial.ttf"):
    """Загрузка шрифта с защитой от ошибок"""
    try:
        return ImageFont.truetype(font_name, size)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

def fit_text(draw, text, max_width, start_size, font_name="arial.ttf"):
    """Подбор размера текста под ширину"""
    size = start_size
    while size > 10:
        font = load_font(size, font_name)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] <= max_width:
            return font
        size -= 2
    return load_font(20, font_name)
def heightmap_to_stl(heightmap, filename, base_mm=3.0, relief_mm=2.0, width_mm=85.0):
    """Превращает 2D карту высот в полноценную 3D модель (с дном и стенками)"""
    # Оптимизация разрешения для стабильной работы слайсеров
    max_res = 350 
    if heightmap.width > max_res:
        aspect = heightmap.height / heightmap.width
        heightmap = heightmap.resize((max_res, int(max_res * aspect)), Image.Resampling.LANCZOS)

    w, h = heightmap.size
    scale = width_mm / w
    pixels = np.array(heightmap) / 255.0
    pixels = np.flipud(pixels) 

    x = np.linspace(0, (w - 1) * scale, w)
    y = np.linspace(0, (h - 1) * scale, h)
    xx, yy = np.meshgrid(x, y)

    # Z-координаты: верх (база + рельеф) и низ (0)
    zz_top = base_mm + pixels * relief_mm
    
    # Расчет количества треугольников (поверхности + стенки)
    num_tri_surface = (w - 1) * (h - 1) * 2
    num_tri_sides = ((w - 1) * 2 + (h - 1) * 2) * 2
    total_tri = num_tri_surface * 2 + num_tri_sides

    data = np.zeros(total_tri, dtype=mesh.Mesh.dtype)
    m = mesh.Mesh(data)

    c = 0
    # 1. Генерация верхней и нижней крышек
    for i in range(h - 1):
        for j in range(w - 1):
            p1, p2 = [xx[i, j], yy[i, j], zz_top[i, j]], [xx[i, j+1], yy[i, j+1], zz_top[i, j+1]]
            p3, p4 = [xx[i+1, j], yy[i+1, j], zz_top[i+1, j]], [xx[i+1, j+1], yy[i+1, j+1], zz_top[i+1, j+1]]
            
            b1, b2 = [xx[i, j], yy[i, j], 0], [xx[i, j+1], yy[i, j+1], 0]
            b3, b4 = [xx[i+1, j], yy[i+1, j], 0], [xx[i+1, j+1], yy[i+1, j+1], 0]
            m.vectors[c] = np.array([p1, p2, p4]); c += 1
            m.vectors[c] = np.array([p1, p4, p3]); c += 1
            # Низ (нормаль вниз)
            m.vectors[c] = np.array([b1, b4, b2]); c += 1
            m.vectors[c] = np.array([b1, b3, b4]); c += 1

    # 2. Боковые стенки (закрываем объем)
    for j in range(w - 1): # По X (верхний и нижний края)
        for i in [0, h-1]:
            v1, v2 = [xx[i, j], yy[i, j], 0], [xx[i, j+1], yy[i, j+1], 0]
            v3, v4 = [xx[i, j], yy[i, j], zz_top[i, j]], [xx[i, j+1], yy[i, j+1], zz_top[i, j+1]]
            m.vectors[c] = np.array([v1, v2, v4]); c += 1
            m.vectors[c] = np.array([v1, v4, v3]); c += 1
    
    for i in range(h - 1): # По Y (левый и правый края)
        for j in [0, w-1]:
            v1, v2 = [xx[i, j], yy[i, j], 0], [xx[i+1, j], yy[i+1, j], 0]
            v3, v4 = [xx[i, j], yy[i, j], zz_top[i, j]], [xx[i+1, j], yy[i+1, j], zz_top[i+1, j]]
            m.vectors[c] = np.array([v1, v4, v2]); c += 1
            m.vectors[c] = np.array([v1, v3, v4]); c += 1

    os.makedirs("output", exist_ok=True)
    m.save(filename)
    return filename
def generate_3d_badge(name, pos, font_name="arial.ttf", base_mm=3.0, relief_mm=1.5):
    """3D Бейдж с логотипом слева и текстом справа"""
    width, height = 850, 550
    img = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(img)

    try:
        logo = Image.open("assets/logo.png").convert("L").resize((240, 240))
        img.paste(logo, (60, 140))
    except:
        draw.text((80, 200), "БрГТУ", fill=255, font=load_font(70, font_name))

    f_name = fit_text(draw, name.upper(), 450, 65, font_name)
    f_pos = load_font(32, font_name)

    draw.text((360, 180), name.upper(), fill=255, font=f_name)
    draw.text((360, 300), pos, fill=180, font=f_pos)

    safe_name = "".join(x for x in name if x.isalnum())[:10]
    return heightmap_to_stl(img, f"output/badge_{safe_name}.stl", base_mm, relief_mm, 85.0)

def generate_3d_icon(font_name="arial.ttf", base_mm=3.0, relief_mm=2.0):
    """Круглый 3D значок"""
    size = 500
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)
    draw.ellipse((20, 20, 480, 480), fill=60) 

    try:
        logo = Image.open("assets/logo.png").convert("L").resize((320, 320))
        img.paste(logo, (90, 90))
    except:
        draw.text((120, 200), "БрГТУ", fill=255, font=load_font(80, font_name))

    return heightmap_to_stl(img, "output/3D_icon.stl", base_mm, relief_mm, 50.0)

def generate_3d_logo_only(font_name="arial.ttf", base_mm=2.0, relief_mm=3.0):
    """Чистый 3D логотип БрГТУ (без фона)"""
    size = 600
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)

    try:
        logo = Image.open("assets/logo.png").convert("L").resize((500, 500))
        img.paste(logo, (50, 50))
    except:
        draw.text((120, 230), "БрГТУ", fill=255, font=load_font(100, font_name))

    return heightmap_to_stl(img, "output/3D_logo_clean.stl", base_mm, relief_mm, 50.0)
