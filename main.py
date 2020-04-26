import tkinter as tk
from settings import settings as ws
from menu_bar import MenuBar
from pages import MainFrame, DefaultEnglishPage, AddWord, QuizPage, Page, SettingsPage


class App:
    """control the main app and in charge to filp page when neede"""
    def __init__(self, window):
        self.main_frame = MainFrame(window)
        self.main_frame.master.bind("<BackSpace>", lambda event: self.go_back())
        self.main_frame.back_o["command"] = self.go_back
        self.menu_bar = MenuBar(window, self.set_home_page,self.set_english_page, self.set_settings_page)

        self.menu_bar.apply()
        self.main_frame.apply()
        self.set_home_page()

    def set_home_page(self):
        self.main_frame.clean_page()
        body = Page(self.main_frame.frame)
        body.add_object(tk.Label, text='HI welcome to Learning Log', height=20, width=25)
        body.apply()
        self.main_frame.update(body.name)

    def set_english_page(self):
        self.main_frame.clean_page()
        body = DefaultEnglishPage(self.main_frame.frame)
        body.btn_pra.config(command=self.set_quiz_page)
        body.btn_add.config(command=self.set_new_word_page)
        self.main_frame.update(body.name)

    def set_new_word_page(self):
        self.main_frame.clean_page()
        body = AddWord(self.main_frame.frame)
        self.main_frame.master.bind('<Return>', body.keypress_handler)
        self.main_frame.update(body.name)

    def set_quiz_page(self):
        self.main_frame.clean_page()
        body = QuizPage(self.main_frame.frame)
        self.main_frame.update(body.name)

    def set_settings_page(self):
        self.main_frame.clean_page()
        body = SettingsPage(self.main_frame.frame)
        self.main_frame.update(body.name)

    def go_back(self):
        last_page = self.main_frame.last_page
        if last_page == "Home":
            self.set_home_page()
        if last_page == "DefaultEnglishPage":
            self.set_english_page()
        if last_page == "QuizPage":
            self.set_quiz_page()


window = tk.Tk()
window.title(ws.title)
window.geometry(ws.win_size)
app = App(window)
window.mainloop()
