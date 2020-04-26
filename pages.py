""" In this module all the templates for the GUI """
import tkinter as tk
from settings import settings as ws
from dict_control import dict_words
from random import randrange
from score import Track
from PIL import ImageTk, Image


class Page:
    def __init__(self, master):
        self.master = master
        self.name = "Home"
        self.bg = ws.body_bg
        self.width = ws.body_width
        self.height = ws.body_height
        self.large_font = ("Helvetica", 18)
        self.frame = tk.Frame(master=self.master, bg=self.bg, width=self.width, height=self.height)
        self.objects = []

        # This object make the frame size constant
        self.anchor = tk.Label(master=self.frame, width=400, height=0, bg=ws.body_bg).pack()

    def apply(self, side=tk.LEFT, fill=tk.BOTH):
        for object_ in self.objects[::-1]:
            object_.pack(side=tk.TOP, padx=2, pady=2)
        self.frame.pack(side=side, fill=fill)

    def add_object(self, object_, text='', width=None, height=None, command=None, font=None):
        if not font:
            font = self.large_font
        if object_ is tk.Entry:
            current = object_(master=self.frame, width=width, font=font)
        else:
            current = object_(text=text, master=self.frame, width=width, height=height, font=font, command=command)

        self.objects.append(current)
        return current

    def clean_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()


class MainFrame(Page):
    def __init__(self, master):
        super().__init__(master)
        self.name = 'MainFrame'
        self.current_page = 'Home'
        self.last_page = []
        self.back_o = self.add_object(tk.Button, text="Back")

    def update(self, page):
        self.last_page = self.current_page
        self.current_page = page
        if self.current_page != "Home":
            self.back_o = self.add_object(tk.Button, text="Back")

    def clean_page(self):
        for widget in self.frame.winfo_children():
            if "!frame" in widget.winfo_name():
                widget.destroy()


class DefaultEnglishPage(Page):
    """ Describe The Default template for the english section in the app"""

    def __init__(self, master):
        super().__init__(master)
        self.name = 'DefaultEnglishPage'
        self.recently_words = dict_words.get_recent_words()
        self.btn_pra = self.add_object(tk.Button, text='Practice', width=50)
        self.btn_add = self.add_object(tk.Button, text='Add new', width=50)
        self.recently_words_handler()
        self.apply()

    def recently_words_handler(self):

        text = '\nRecently Words\n' + '=' * 30 + '\n'
        for word, trans in self.recently_words.items():
            text += word.capitalize() + '\t' + trans + '\n'

        self.add_object(tk.Label, text=text, width=50)


class AddWord(Page):
    """ Describe template form for adding new word to the list"""
    def __init__(self, master):
        super().__init__(master)
        self.name = 'AddWord'
        self.add_object(tk.Label, text='new word', width=15, height=2)
        self.new_word = self.add_object(tk.Entry, width=50, height=2)
        self.add_object(tk.Label, text='Translation', width=15, height=2)
        self.new_trans = self.add_object(tk.Entry, width=50, height=2)
        self.add_object(tk.Button, text='save', width=50, command=self.save)
        self.apply()

    def save(self):
        new_tran = self.new_word.get().strip().capitalize()
        new_word = self.new_trans.get().strip()
        if new_word and new_tran:
            dict_words.add_entry({new_word: new_tran})

    def keypress_handler(self, event):
        if event.keysym == 'Return':
            self.save()


class QuizPage(Page):
    """ Describe a template for quiz page and handle scoring"""

    def __init__(self, master):
        super().__init__(master)
        self.name = "QuizPage"
        self.dict_words = dict_words.get_dict()
        self.word_list = list(self.dict_words.keys())
        self.track = Track()

        self.score_o = self.add_object(tk.Label, width=15)
        # create objects list for answers
        self.answers_o = self.create_answers_o()
        self.word_o = self.add_object(tk.Label, width=50)

        # Config objects
        self.new_quest()

        self.apply()

    def gen_answers(self):
        """
        Generate rand answers and make sure you have the right inside and you don't have
        the same answer twice
        """
        answers = [None for i in range(4)]
        answers[randrange(0, 4)] = self.dict_words[self.r_word]
        for i, an in enumerate(answers):
            while not an:
                answer = self.dict_words[self.gen_rand_word()]
                if answer not in answers:
                    an = answer
                    answers[i] = an

        return answers

    def gen_rand_word(self):
        """Return a random word from the dict and make sure it had
        nod not been asked at least in the 10 question before"""

        r_index = randrange(len(self.word_list))
        r_word = self.word_list[r_index]
        return r_word if r_word not in self.track.last_questioned else self.gen_rand_word()

    def create_answers_o(self):
        """ Create 4 button tkinter objects for answers """
        answers = []
        for answer in range(4):
            object_ = self.add_object(tk.Button, width=50)
            object_.config(command=lambda answer=answer, object_=object_: self.check_answer(answer, object_))
            answers.append(object_)
        return answers

    def check_answer(self, answer, object_):
        """ Check answer and call for the next one """
        if self.dict_words[self.r_word] == answer:
            fail = None

        else:
            fail = self.r_word

        self.track.update(self.r_word, fail=fail)
        self.new_quest()

    def new_quest(self):
        """ Config the objects for answers and the question """
        # Generate rand question
        self.r_word = self.gen_rand_word()
        self.answers = self.gen_answers()

        # config question object with the proper text and the question
        text = f"What is the right translation ?\n{'=' * 30}\n{self.r_word}"
        self.word_o.config(text=text)

        # Config answers objects
        for i, o in enumerate(self.answers_o):
            answer = self.answers[i]
            o.config(text=answer,
                     command=lambda answer=answer, object_=o: self.check_answer(answer, object_))
        # Update Score
        self.score_o.config(text=f'Your score: {self.track.score}\nYour avg.: {self.track.get_average_success()}')

class SettingsPage:
    def __init__(self, master):
        self.name = 'Settings'
        self.i = ImageTk.PhotoImage(Image.open("./images/view.jpg"))
        self.f = tk.Frame(master=master, width=100)
        self.l = tk.Label(master=self.f, text='LLLL')
        self.f.pack()

