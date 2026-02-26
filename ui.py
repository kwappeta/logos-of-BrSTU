import tkinter as tk
from tkinter import messagebox
from badge_generator import generate_badge
from logo_generator import generate_logo

def run_ui():
    root = tk.Tk()
    root.title("Генератор значков и логотипов БрГТУ")
    root.geometry("520x520")
    root.resizable(False, False)
    
    # Заголовок
    tk.Label(root, text="Производственная система БрГТУ", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Выбор режима
    mode_var = tk.StringVar(value="badge")
    tk.Label(root, text="Режим:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10,0))
    
    tk.Radiobutton(root, text="Бейджик", variable=mode_var, value="badge", font=("Arial", 12)).pack(anchor="w", padx=40)
    tk.Radiobutton(root, text="Логотип/Значок", variable=mode_var, value="logo", font=("Arial", 12)).pack(anchor="w", padx=40)
    
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
    tk.Radiobutton(variant_frame, text="Цветной", variable=variant_var, value="colored").pack(side="left", padx=5)
    tk.Radiobutton(variant_frame, text="Только текст", variable=variant_var, value="text_only").pack(side="left", padx=5)
    
    # Функция генерации
    def on_generate():
        mode = mode_var.get()
        if mode == "badge":
            name = entry_name.get().strip()
            position = entry_pos.get().strip()
            
            if not name:
                messagebox.showwarning("Ошибка", "Введите ФИО!")
                return
            
            filename = generate_badge(name, position)
            messagebox.showinfo("Готово!", f"Значок сохранён:\n{filename}")
        else:
            variant = variant_var.get()
            filename = generate_logo(variant)
            messagebox.showinfo("Готово!", f"Логотип сохранён:\n{filename}")
    
    # Кнопка генерации
    tk.Button(root, text="СГЕНЕРИРОВАТЬ", command=on_generate,
              font=("Arial", 16, "bold"), bg="#4da6ff", fg="white", width=20, height=2).pack(pady=25)
    
    root.mainloop()
