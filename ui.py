import customtkinter as ctk
from tkinter import colorchooser, messagebox

# Импорт генераторов
from badge_generator import generate_badge
from logo_generator import generate_logo
from stl_generator import generate_3d_badge, generate_3d_icon, generate_3d_logo_only

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Производственная система БрГТУ v2.0")
        self.geometry("740x760")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.badge_color = ctk.StringVar(value="#0056b3")
        self.logo_mode = ctk.StringVar(value="logo_text")

        # Заголовок
        self.header = ctk.CTkLabel(self, 
                                   text="Система автоматизации производства БрГТУ",
                                   font=ctk.CTkFont(size=23, weight="bold"))
        self.header.pack(pady=20)

        # Вкладки
        self.tabview = ctk.CTkTabview(self, width=700, height=560)
        self.tabview.pack(pady=10, padx=25, fill="both", expand=True)

        self.tab_badge = self.tabview.add("   Бейджи   ")
        self.tab_logo = self.tabview.add("   Значки и Лого   ")

        self.setup_badge_tab()
        self.setup_logo_tab()

        # Кнопка генерации
        self.generate_button = ctk.CTkButton(self,
                                             text="СОЗДАТЬ / СГЕНЕРИРОВАТЬ",
                                             font=ctk.CTkFont(size=19, weight="bold"),
                                             height=65,
                                             fg_color="#003366",
                                             hover_color="#002244",
                                             corner_radius=12,
                                             command=self.on_generate)
        self.generate_button.pack(pady=20, padx=40, fill="x")
    def setup_badge_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_badge)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll, text="Персонализация бейджа", 
                     font=ctk.CTkFont(size=17, weight="bold")).pack(pady=(20, 12), padx=25, anchor="w")

        ctk.CTkLabel(scroll, text="ФИО:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=30, pady=(8, 4))
        self.entry_name = ctk.CTkEntry(scroll, height=42, font=ctk.CTkFont(size=14))
        self.entry_name.pack(fill="x", padx=30, pady=5)
        self.entry_name.insert(0, "Иванов Иван Иванович")

        ctk.CTkLabel(scroll, text="Группа / Должность:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=30, pady=(12, 4))
        self.entry_pos = ctk.CTkEntry(scroll, height=42, font=ctk.CTkFont(size=14))
        self.entry_pos.pack(fill="x", padx=30, pady=5)
        self.entry_pos.insert(0, "22-ИТ-1")

        # Цвет бейджа
        c = ctk.CTkFrame(scroll)
        c.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(c, text="Цвет рамки и надписи:", width=180, anchor="w").pack(side="left", padx=10)
        self.color_btn = ctk.CTkButton(c, text="Выбрать цвет", 
                                       fg_color=self.badge_color.get(),
                                       command=self.choose_color)
        self.color_btn.pack(side="left", padx=10)

        # Тип изготовления
        ctk.CTkLabel(scroll, text="Тип изготовления:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=30, pady=(20, 8))
        self.badge_type = ctk.StringVar(value="2d")
        ctk.CTkRadioButton(scroll, text="2D бейдж (PNG)", variable=self.badge_type, value="2d").pack(anchor="w", padx=45, pady=5)
        ctk.CTkRadioButton(scroll, text="3D бейдж (STL)", variable=self.badge_type, value="3d").pack(anchor="w", padx=45, pady=5)

        # Параметры 3D
        self.frame_3d = ctk.CTkFrame(scroll)
        self.frame_3d.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(self.frame_3d, text="Параметры 3D (мм)").pack(pady=5)
        
        self.entry_base = ctk.CTkEntry(self.frame_3d, width=100)
        self.entry_base.pack(side="left", padx=20, pady=10)
        self.entry_base.insert(0, "4.0")
        
        self.entry_relief = ctk.CTkEntry(self.frame_3d, width=100)
        self.entry_relief.pack(side="left", padx=20, pady=10)
        self.entry_relief.insert(0, "2.5")
    def setup_logo_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_logo)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll, text="Генерация значков и логотипов", 
                     font=ctk.CTkFont(size=17, weight="bold")).pack(pady=20)

        f2 = ctk.CTkFrame(scroll)
        f2.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkRadioButton(f2, text="Текстовый логотип (PNG)", variable=self.logo_mode, value="logo_text").pack(anchor="w", padx=40, pady=7)
        ctk.CTkRadioButton(f2, text="Чистый логотип (STL)", variable=self.logo_mode, value="logo_stl").pack(anchor="w", padx=40, pady=7)

        self.logo_mode.trace("w", self.update_color_option)
        self.update_color_option()

    def update_color_option(self, *args):
        pass  # Цвет пока не используется в лого

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.badge_color.get())[1]
        if color:
            self.badge_color.set(color)
            self.color_btn.configure(fg_color=color)

    def on_generate(self):
        current_tab = self.tabview.get()

        try:
            base = float(self.entry_base.get() or 4.0)
            relief = float(self.entry_relief.get() or 2.5)

            if "Бейджи" in current_tab:
                name = self.entry_name.get().strip()
                pos = self.entry_pos.get().strip()
                if not name:
                    messagebox.showerror("Ошибка", "Введите ФИО!")
                    return

                if self.badge_type.get() == "2d":
                    # Исправленный вызов — теперь 3 аргумента
                    result = generate_badge(name, pos, self.badge_color.get())
                else:
                    result = generate_3d_badge(name, pos, base, relief)

            else:  # Лого
                mode = self.logo_mode.get()
                if mode == "logo_text":
                    result = generate_logo("text_only")
                elif mode == "logo_stl":
                    result = generate_3d_logo_only(base, relief)

            messagebox.showinfo("Успех ✓", f"Файл успешно создан:\n{result}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Критическая ошибка:\n{str(e)}")

def run_ui():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    run_ui()
