import numpy as np
from PIL import Image, ImageDraw, ImageFont
from stl import mesh
import os


def load_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()


def fit_text(draw, text, max_width, start_size):
    size = start_size
    while size > 10:
        font = load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] <= max_width:
            return font
        size -= 2
    return load_font(20)


def heightmap_to_stl(heightmap, filename, base_mm=4.0, relief_mm=2.5, width_mm=85.0):
    w, h = heightmap.size
    scale = width_mm / w

    pixels = np.array(heightmap)

    pixels = np.flipud(pixels)

    pixels = pixels / 255.0

    pixels = 1.0 - pixels

    x = np.linspace(0, w * scale, w)
    y = np.linspace(0, h * scale, h)
    xx, yy = np.meshgrid(x, y)

    zz = base_mm + pixels * relief_mm

    num_tri = (w - 1) * (h - 1) * 2
    data = np.zeros(num_tri, dtype=mesh.Mesh.dtype)
    m = mesh.Mesh(data)

    c = 0
    for i in range(h - 1):
        for j in range(w - 1):
            p1 = [xx[i, j], yy[i, j], zz[i, j]]
            p2 = [xx[i, j+1], yy[i, j+1], zz[i, j+1]]
            p3 = [xx[i+1, j], yy[i+1, j], zz[i+1, j]]
            p4 = [xx[i+1, j+1], yy[i+1, j+1], zz[i+1, j+1]]

            m.vectors[c] = np.array([p1, p2, p4])
            m.vectors[c+1] = np.array([p1, p4, p3])
            c += 2

    os.makedirs("output", exist_ok=True)
    m.save(filename)
    return filename


def generate_3d_badge(name, pos, base_mm=4.0, relief_mm=2.5):
    width, height = 850, 550
    img = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(img)

    # --- ЛОГО СЛЕВА ---
    try:
        logo = Image.open("assets/logo.png").convert("L")
        logo = logo.resize((260, 260))
        img.paste(logo, (60, 140))
    except:
        draw.text((120, 250), "LOGO", fill=255, font=load_font(80))

    # --- ТЕКСТ СПРАВА ---
    font_name = fit_text(draw, name, 400, 65)
    font_pos = load_font(40)

    draw.text((380, 200), name, fill=255, font=font_name)
    draw.text((380, 320), pos, fill=200, font=font_pos)

    safe = name.replace(" ", "_")[:10]
    return heightmap_to_stl(img, f"output/3D_badge_{safe}.stl", base_mm, relief_mm, 85.0)



def generate_3d_icon(base_mm=3.0, relief_mm=2.0):
    size = 500
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)

    # КРУГ
    draw.ellipse((10, 10, size-10, size-10), fill=30)

    # ЛОГО
    try:
        logo = Image.open("assets/logo.png").convert("L")
        logo = logo.resize((300, 300))
        img.paste(logo, (100, 100))
    except:
        draw.text((120, 220), "БрГТУ", fill=255, font=load_font(80))

    return heightmap_to_stl(img, "output/3D_icon.stl", base_mm, relief_mm, 50.0)


def generate_3d_logo_only(base_mm=2.0, relief_mm=3.0):
    try:
        img = Image.open("assets/logo.png").convert("L")
        img = img.resize((500, 500))
    except:
        img = Image.new('L', (500, 500), 0)
        draw = ImageDraw.Draw(img)
        draw.text((120, 200), "LOGO", fill=255, font=load_font(100))

    return heightmap_to_stl(img, "output/3D_logo.stl", base_mm, relief_mm, 50.0)
