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

        self.request_screen()

    def main_screen(self):

        w = int(self.root.winfo_screenwidth())
        h = int(self.root.winfo_screenheight())

        print(w,h)

        self.main_cont = Frame(self.root, width=w, height=h, borderwidth=1, relief=SOLID)
        self.main_cont.pack(fill=BOTH)
        self.head_frame = Frame(self.main_cont, width=w, height=h, borderwidth=1, relief=SOLID)
        self.head_frame.pack(anchor=E, fill=X)
        self.main_frame = Frame(self.main_cont, width=w, height=h, pady=h*0.3, borderwidth=1, relief=SOLID)
        self.main_frame.pack(anchor=CENTER, fill=X)
        
        exit_button = Button(self.head_frame, text="Выход", command=self.root.destroy, width=10, height=2).pack(anchor=E)
        client_button = Button(self.main_frame ,text="Вход для Клиента", command= self.user, width=40, height=5).pack(anchor=CENTER)
        register_button = Button(self.main_frame, text="Регистрация Клиента", command=self.register, width=40, height=5).pack(anchor=CENTER, pady=10)
        worker_button = Button(self.main_frame ,text="Вход для Рабочего", command= self.rabochi, width=40, height=5).pack(anchor=CENTER)


    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    
    def default_login_screen(self, frame):
        back_button = Button(self.head_frame, text="Назад", command=self.back_func, width=10, height=2)
        back_button.pack(anchor=E)
        log_text_rab = Label(frame, text="Логин:", font=('Arial 18'))
        log_text_rab.grid(sticky=W, row=0, column=0, columnspan=3)
        login_rab = Entry(frame, name="login_value", width=30, font=('Arial 22'))
        login_rab.grid(row=1, column=0, columnspan=2)
        
        pass_text_rab = Label(frame, text="Пароль:", font=('Arial 18'))
        pass_text_rab.grid(sticky=W,row=2, column=0, columnspan=3)
        password_rab = Entry(frame, name="password", width=30, font=('Arial 22'), show="▓")
        password_rab.grid(row=3, column=0, columnspan=2)
        Button(frame, width=3, height=1, command=self.hide_password).grid(padx=5, row=3, column=2)
        

    def user(self):
        self.clear_window()
        user_frame = Frame(self.main_frame, name="user_login")
        user_frame.pack(anchor=CENTER)
        self.default_login_screen(user_frame)

        enter_rab_button = Button(user_frame, text="Вход", width=20, height=3, command=self.user_authentication).grid(pady=20, row=6, column=0, columnspan=2)
    
    def rabochi(self):
        self.clear_window()
        rab_frame = Frame(self.main_frame, name="worker_login")
        rab_frame.pack(anchor=CENTER)
        self.default_login_screen(rab_frame)

        enter_rab_button = Button(rab_frame, text="Вход", width=20, height=3, command=self.admin_authentication).grid(pady=20, row=6, column=0, columnspan=2)

    def register(self):
        self.clear_window()
        register_frame= Frame(self.main_frame, name="register")
        register_frame.pack(anchor=CENTER)
        self.default_login_screen(register_frame)

        repeat_password_label= Label(register_frame, text="Повторите пароль:", font=('Arial 18')).grid(sticky=W,row=4, column=0, columnspan=3)
        repeat_password_rab = Entry(register_frame, name="repeat_password", width=30, font=('Arial 22'), show="▓").grid(row=5, column=0, columnspan=2)
        registred_button = Button(register_frame, text="регистрация", width=20, height=3, command=self.registred_user).grid(pady=20, row=6, column=0, columnspan=2)

    def hide_password(self):
        login_window = self.main_frame.children.get("worker_login") or self.main_frame.children.get("user_login") or self.main_frame.children.get("register")
        for password_key in ["password", "repeat_password"]:
            password = login_window.children.get(password_key)
            if password:
                print(password.cget('show'))
                if password.cget('show') == '':
                    password.config(show="▓")
                else:
                    password.config(show="")
            else:
                continue

    def user_authentication(self):
        get_value = self.main_frame.children.get("user_login")
        login_value = get_value.children.get("login_value").get()
        password_value = get_value.children.get("password").get()
        password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
        if db.search_user_for_login(login_value, password_value):
            print('done')
        else:
            print('not')
        db.check_log_in()

    def registred_user(self):
        get_value = self.main_frame.children.get("register")
        login_value = get_value.children.get("login_value").get()
        password_value = get_value.children.get("password").get()
        repeat_password = get_value.children.get("repeat_password").get()
        if password_value == repeat_password:
            password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
            print(login_value, password_value)
            if not db.check_and_get_user(login_value):
                db.insert_value(login_value, password_value)
            else:
                messagebox.showwarning(title='nini', message='пользователь с таким логином есть')
        else:
            messagebox.showwarning(title='nini', message='пароли не совпадают')
        db.check_log_in()

    def admin_authentication(self):
        get_value = self.main_frame.children.get("worker_login")
        login_value = get_value.children.get("login_value").get()
        password_value = get_value.children.get("password").get()
        password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
        if db.search_admin_for_login(login_value, password_value):
            print('done')
        else:
            print('not')
        db.check_log_in()


    def request_screen(self):
        # очистка main_frame
        self.clear_window()
        # очистка head_frame 
        for widget in self.head_frame.winfo_children():
            widget.destroy()

        search_line = Entry(self.head_frame, name="search_line", font=('Arial 22')).grid(row=0, column=0, columnspan=4)
        search_button = Button(self.head_frame, text="Поиск", name = "search_button", width=10, height=2).grid(row=0, column=4)
        
        request_screen_frame = Frame(self.main_frame, name="request")


        
    def back_func(self):
        self.main_cont.pack_forget()
        self.head_frame.pack(anchor=E, fill=X)
        self.main_screen()

    def run(self):
        self.root.mainloop()
    
a = App()
a.run()
