from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import hashlib
import db
from setings import password_salt

class App():

    def __init__(self):
        
        root = Tk()
        root.title("Приложение на Tkinter")
        root.geometry("1920x1080")
        root.attributes("-fullscreen", True) 

        self.root= root
    
        self.test_screen()

    def test_screen(self):
        w = int(self.root.winfo_screenwidth())
        h = int(self.root.winfo_screenheight())

        self.main_cont = Frame(self.root, width=w, height=h, borderwidth=1, relief=SOLID)
        self.main_cont.pack(fill=BOTH)
        self.head_frame = Frame(self.main_cont, width=w, height=h, borderwidth=1, relief=SOLID)
        self.head_frame.pack(anchor=E, fill=X)
        self.main_frame = Frame(self.main_cont, width=w, height=h, pady=h*0.3, borderwidth=1, relief=SOLID)
        self.main_frame.pack(anchor=CENTER, fill=X)
        back_button = Button(self.head_frame, text="Назад", width=10, height=2)
        back_button.pack(anchor=E)

    def run(self):
        self.root.mainloop()

    
a = App()
a.run()
