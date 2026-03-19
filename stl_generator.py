import numpy as np
from PIL import Image, ImageDraw, ImageFont
from stl import mesh
import os

def create_base_image(size, shape="rect"):
    """Создает черную подложку: rect (прямоугольник) или circle (круг)"""
    img = Image.new('L', size, 0)
    draw = ImageDraw.Draw(img)
    if shape == "circle":
        draw.ellipse([0, 0, size[0]-1, size[1]-1], fill=0) # Фон всегда 0
    return img

def add_text_to_image(img, text, position, font_size, align="center"):
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Рисуем текст белым цветом (255 = максимальный рельеф)
    draw.text(position, text, fill=255, font=font, anchor="mm" if align=="center" else "la")
    return img

def heightmap_to_stl(heightmap, stl_filename, base_mm=4.0, relief_mm=2.5, physical_width=85.0):
    w, h = heightmap.size
    scale = physical_width / w
    pixels = np.array(heightmap) / 255.0

    x = np.linspace(0, w * scale, w)
    y = np.linspace(0, h * scale, h)
    xx, yy = np.meshgrid(x, y)
    
    # Z = База + Рельеф. Если пиксель черный (0), будет только база.
    zz = base_mm + (pixels * relief_mm)

    # Генерация сетки треугольников
    num_triangles = (w - 1) * (h - 1) * 2
    data = np.zeros(num_triangles, dtype=mesh.Mesh.dtype)
    m = mesh.Mesh(data)

    counter = 0
    for i in range(h - 1):
        for j in range(w - 1):
            # Вершины квадрата (пикселя)
            p1 = [xx[i, j], yy[i, j], zz[i, j]]
            p2 = [xx[i, j+1], yy[i, j+1], zz[i, j+1]]
            p3 = [xx[i+1, j], yy[i+1, j], zz[i+1, j]]
            p4 = [xx[i+1, j+1], yy[i+1, j+1], zz[i+1, j+1]]

            m.vectors[counter] = np.array([p1, p2, p4])
            m.vectors[counter + 1] = np.array([p1, p4, p3])
            counter += 2

    if not os.path.exists("output"): os.makedirs("output")
    m.save(stl_filename)
    return stl_filename


def generate_3d_badge(name, pos, base_mm, relief_mm):
    """Прямоугольный бейдж 85x55мм"""
    img = Image.new('L', (850, 550), 0)
    add_text_to_image(img, name, (425, 200), 60)
    add_text_to_image(img, pos, (425, 350), 40)
    return heightmap_to_stl(img, f"output/3D_Badge_{name[:10]}.stl", base_mm, relief_mm, 85.0)

def generate_3d_icon(base_mm, relief_mm):
    """Круглый значок (диаметр 50мм) с логотипом"""
    size = (500, 500)
    img = Image.new('L', size, 0)
    draw = ImageDraw.Draw(img)
    # Рисуем круг (маска)
    draw.ellipse([10, 10, 490, 490], outline=255, width=5)
    # Пытаемся наложить логотип (если есть) или просто текст БрГТУ
    add_text_to_image(img, "БрГТУ", (250, 250), 80)
    return heightmap_to_stl(img, "output/3D_Icon_BrGTU.stl", base_mm, relief_mm, 50.0)

def generate_3d_logo_only(base_mm, relief_mm):
    """Чистый логотип (без рамки)"""
    # Загружаем ваш logo.png и конвертируем в L
    try:
        img = Image.open("assets/logo.png").convert('L')
        img = img.resize((500, 500))
    except:
        img = Image.new('L', (500, 500), 0)
        add_text_to_image(img, "LOGO", (250, 250), 100)
        
    return heightmap_to_stl(img, "output/3D_Logo_Pure.stl", base_mm, relief_mm, 50.0)
