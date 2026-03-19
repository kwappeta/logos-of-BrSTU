import tkinter as tk
from tkinter import ttk, messagebox
from badge_generator import generate_badge
from logo_generator import generate_logo
from stl_generator import generate_3d_badge, generate_3d_icon, generate_3d_logo_only

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Производственная система БрГТУ v2.0")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        
        header = tk.Label(root, text="Система автоматизации БрГТУ", font=("Arial", 16, "bold"), fg="#0056b3")
        header.pack(pady=10)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Вкладка 1: Бейджи
        self.tab_badge = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_badge, text=" Бейджи ")
        self.setup_badge_tab()

        # Вкладка 2: Значки и Лого
        self.tab_logo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_logo, text=" Значки / Лого ")
        self.setup_logo_tab()

        self.btn_gen = tk.Button(root, text="СГЕНЕРИРОВАТЬ ВЫБРАННОЕ", command=self.on_generate,
                                 font=("Arial", 14, "bold"), bg="#4da6ff", fg="white", height=2)
        self.btn_gen.pack(fill="x", padx=20, pady=20)

    def setup_badge_tab(self):
        tk.Label(self.tab_badge, text="Данные персонализации", font=("Arial", 11, "bold")).pack(pady=10)
        
        tk.Label(self.tab_badge, text="ФИО:").pack()
        self.entry_name = tk.Entry(self.tab_badge, width=40, font=("Arial", 12))
        self.entry_name.pack(pady=5)
        self.entry_name.insert(0, "Иванов Иван Иванович")

        tk.Label(self.tab_badge, text="Группа:").pack()
        self.entry_pos = tk.Entry(self.tab_badge, width=40, font=("Arial", 12))
        self.entry_pos.pack(pady=5)
        self.entry_pos.insert(0, "22-ИТ-1")

        tk.Label(self.tab_badge, text="Тип производства:", font=("Arial", 10, "bold")).pack(pady=10)
        self.badge_type = tk.StringVar(value="2d")
        tk.Radiobutton(self.tab_badge, text="Обычный бейдж (PNG)", variable=self.badge_type, value="2d").pack()
        tk.Radiobutton(self.tab_badge, text="Объемный бейдж (STL)", variable=self.badge_type, value="3d").pack()

        self.frame_3d_settings(self.tab_badge)

    def setup_logo_tab(self):
        tk.Label(self.tab_logo, text="Выберите тип и формат изделия", font=("Arial", 11, "bold")).pack(pady=15)
        
        self.logo_mode = tk.StringVar(value="icon_png")
        
        # Блок PNG (2D)
        tk.Label(self.tab_logo, text="--- Растровая графика (2D) ---", fg="blue").pack()
        tk.Radiobutton(self.tab_logo, text="Круглый значок БрГТУ (PNG)", 
                       variable=self.logo_mode, value="icon_png", font=("Arial", 10)).pack(pady=5)
        tk.Radiobutton(self.tab_logo, text="Чистый логотип (PNG)", 
                       variable=self.logo_mode, value="logo_png", font=("Arial", 10)).pack(pady=5)
        
        # Разделитель
        tk.Label(self.tab_logo, text="").pack()

        # Блок STL (3D)
        tk.Label(self.tab_logo, text="--- Модели для печати (3D) ---", fg="blue").pack()
        tk.Radiobutton(self.tab_logo, text="Круглый значок БрГТУ (STL)", 
                       variable=self.logo_mode, value="icon_stl", font=("Arial", 10)).pack(pady=5)
        tk.Radiobutton(self.tab_logo, text="Чистый логотип (STL)", 
                       variable=self.logo_mode, value="logo_stl", font=("Arial", 10)).pack(pady=5)

    def frame_3d_settings(self, parent):
        group = tk.LabelFrame(parent, text="Параметры 3D модели (мм)")
        group.pack(pady=15, padx=20, fill="x")
        
        tk.Label(group, text="Толщина базы:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_base = tk.Entry(group, width=8)
        self.entry_base.grid(row=0, column=1)
        self.entry_base.insert(0, "4.0")

        tk.Label(group, text="Высота рельефа:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_relief = tk.Entry(group, width=8)
        self.entry_relief.grid(row=1, column=1)
        self.entry_relief.insert(0, "2.5")

    def on_generate(self):
        tab = self.notebook.index(self.notebook.select())
        
        try:
            b, r = float(self.entry_base.get()), float(self.entry_relief.get())
        except:
            b, r = 4.0, 2.5

        if tab == 0: # Бейджи
            name, pos = self.entry_name.get().strip(), self.entry_pos.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Заполните ФИО")
                return
            res = generate_badge(name, pos) if self.badge_type.get() == "2d" else generate_3d_badge(name, pos, b, r)
        
        else: # Значки / Лого
            mode = self.logo_mode.get()
            if mode == "icon_png":
                res = generate_logo("classic") # Вызывает генерацию классического значка
            elif mode == "logo_png":
                res = generate_logo("colored") # Или "text_only" в зависимости от настроек
            elif mode == "icon_stl":
                res = generate_3d_icon(b, r)
            elif mode == "logo_stl":
                res = generate_3d_logo_only(b, r)

        messagebox.showinfo("Успех", f"Файл успешно создан:\n{res}")

def run_ui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    run_ui()
