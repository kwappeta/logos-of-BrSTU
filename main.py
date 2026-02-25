from ui import run_ui

if __name__ == "__main__":
    run_ui()
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import messagebox
import os

# Размеры бейджа (85×55 мм при ~300 dpi)
BADGE_WIDTH, BADGE_HEIGHT = 1000, 640

# Размер логотипа (квадратный)
LOGO_SIZE = 800

# Глобальные шрифты (лучше положить arial.ttf рядом с main.py)
try:
    font_big    = ImageFont.truetype("arial.ttf", 80)
    font_medium = ImageFont.truetype("arial.ttf", 50)
    font_small  = ImageFont.truetype("arial.ttf", 40)
except Exception:
    font_big    = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small  = ImageFont.load_default()


def generate_badge():
    name = entry_name.get().strip()
    position = entry_pos.get().strip()
    
    if not name:
        messagebox.showwarning("Ошибка", "Введите ФИО!")
        return
    
    # Создаём белый фон
    img = Image.new('RGB', (BADGE_WIDTH, BADGE_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    
    # Логотип
    try:
        logo = Image.open("assets/logo.png").convert("RGBA")
        logo = logo.resize((350, 350))
        img.paste(logo, (70, 140), logo)
    except:
        draw.text((80, 200), "[ЛОГОТИП]", fill="black", font=font_medium)
    
    # Текст
    draw.text((480, 160), name.upper(), fill="black", font=font_big)
    draw.text((480, 270), position, fill="gray", font=font_medium)
    draw.text((480, 370), "БрГТУ", fill="blue", font=font_small)
    
    # Рамка
    draw.rectangle([(20, 20), (BADGE_WIDTH-20, BADGE_HEIGHT-20)], outline="blue", width=8)
    
    # Сохранение
    os.makedirs("output", exist_ok=True)
    filename = f"output/badge_{name.replace(' ', '_').replace('.', '')}.png"
    img.save(filename)
    messagebox.showinfo("Готово!", f"Значок сохранён:\n{filename}")


def generate_logo():
    variant = variant_var.get()
    
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
    
    elif variant == "colored":
        bg_color = (0, 51, 160)  # тёмно-синий (пример фирменного цвета БрГТУ)
        img = Image.new('RGB', (LOGO_SIZE, LOGO_SIZE), color=bg_color)
        draw = ImageDraw.Draw(img)
        if logo_base:
            img.paste(logo_base, (110, 110), logo_base)
        draw.text((140, 680), "БрГТУ", fill="white", font=font_big)
    
    elif variant == "text_only":
        draw.text((80, 180), "БрГТУ", fill="blue", font=ImageFont.truetype("arial.ttf", 180) if "arial.ttf" in globals() else font_big)
        draw.text((80, 380), "Брестский государственный", fill="gray", font=font_medium)
        draw.text((80, 440), "технический университет", fill="gray", font=font_medium)
    
    # Сохранение
    os.makedirs("output", exist_ok=True)
    filename = f"output/logo_{variant}.png"
    img.save(filename)
    messagebox.showinfo("Готово!", f"Логотип сохранён:\n{filename}")


root = tk.Tk()
root.title("Генератор значков и логотипов БрГТУ")
root.geometry("520x520")
root.resizable(False, False)

# Заголовок
tk.Label(root, text="Производственная система БрГТУ", font=("Arial", 16, "bold")).pack(pady=10)

# Выбор режима
mode_var = tk.StringVar(value="badge")
tk.Label(root, text="Режим:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10,0))

tk.Radiobutton(root, text="Значок (бейдж)", variable=mode_var, value="badge", font=("Arial", 12)).pack(anchor="w", padx=40)
tk.Radiobutton(root, text="Логотип",       variable=mode_var, value="logo",   font=("Arial", 12)).pack(anchor="w", padx=40)

# Поля для бейджа
tk.Label(root, text="ФИО:", font=("Arial", 11)).pack(pady=(15,0))
entry_name = tk.Entry(root, width=38, font=("Arial", 14))
entry_name.pack(pady=5)

tk.Label(root, text="Должность / группа:", font=("Arial", 11)).pack()
entry_pos = tk.Entry(root, width=38, font=("Arial", 14))
entry_pos.pack(pady=5)

# Варианты логотипа
variant_frame = tk.Frame(root)
variant_frame.pack(pady=15)

variant_var = tk.StringVar(value="classic")
tk.Label(variant_frame, text="Вариант логотипа:", font=("Arial", 11)).pack(side="left", padx=10)

tk.Radiobutton(variant_frame, text="Классический", variable=variant_var, value="classic").pack(side="left", padx=5)
tk.Radiobutton(variant_frame, text="Цветной",      variable=variant_var, value="colored").pack(side="left", padx=5)
tk.Radiobutton(variant_frame, text="Только текст", variable=variant_var, value="text_only").pack(side="left", padx=5)

# Кнопка
def on_generate():
    mode = mode_var.get()
    if mode == "badge":
        generate_badge()
    else:
        generate_logo()

tk.Button(root, text="СГЕНЕРИРОВАТЬ", command=on_generate,
          font=("Arial", 16, "bold"), bg="#4da6ff", fg="white", width=20, height=2).pack(pady=25)

root.mainloop()
