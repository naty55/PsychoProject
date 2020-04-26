import tkinter as tk
from settings import settings as ws


class MenuBar:
    def __init__(self, master, home_btn, english_btn, settings_btn):
        self.master = master
        self.btn_width = ws.menu_btn_width
        self.btn_clr = ws.menu_btn_clr
        self.root = tk.Frame(master=master, bg=ws.menu_bar_bg, width=ws.menu_bar_width, height=ws.menu_bar_height)

        self.btn_home = self.create_button(text='Home', command=home_btn)
        self.btn_add = self.create_button(text='+ Add new', command=self.add_button)
        self.btn_english = self.create_button(text='English', command=english_btn)
        self.btn_settings = self.create_button(text='settings', command=settings_btn)

        self.buttons = []

    def create_button(self, text, command):
        return tk.Button(master=self.root, text=text, bg=ws.menu_btn_clr,
                         width=ws.menu_btn_width,  height=ws.menu_btn_height,
                         relief=tk.FLAT, borderwidth=1, command=command, activebackground='grey',
                         font=('Comic Sans', 14))

    def apply(self):
        self.root.pack(fill=tk.Y, side=tk.LEFT, expand=True)
        self.btn_home.pack(padx=2, pady=2)
        self.btn_english.pack(padx=2, pady=2)
        self.btn_settings.pack(padx=2, pady=2)
        self.btn_add.pack(padx=2, pady=2)

    def add_button(self):
        pass