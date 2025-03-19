from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import hashlib
from system import password_salt, today
import mydb

class App():

    def __init__(self):
        
        root = Tk()
        root.title("Приложение на Tkinter")
        root.geometry("1920x1080")
        root.attributes("-fullscreen", True) 

        self.root= root

        w = int(self.root.winfo_screenwidth())
        h = int(self.root.winfo_screenheight())

        self.main_frame = Frame(self.root, width=w, height=h, borderwidth=1, relief=SOLID)
        self.main_frame.pack(fill=BOTH)
        self.head_frame = Frame(self.main_frame, width=w, height=h, borderwidth=1, relief=SOLID)
        self.head_frame.pack(fill=X, anchor=E)
        self.body_frame = Frame(self.main_frame, width=w, height=h, borderwidth=1, relief=SOLID)
        self.body_frame.pack(fill=X, anchor=CENTER)

        self.request_screen('ddd', 'user')
        
    def clear_body(self):
        for widget in self.body_frame.winfo_children():
            widget.destroy()
    def clear_head(self):
        for widget in self.head_frame.winfo_children():
            widget.destroy()
    def clear_main(self):
        self.clear_body()
        self.clear_head()

    def main_screen(self):
        self.clear_main()

        Button(self.head_frame, text="Выход", font=('Arial 10'), width=10, height=2, command=self.root.destroy).pack(anchor=E)

        Button(self.body_frame, text="Вход для клиента", font=('Arial 12'), width=30, height=3, command=self.user_login_screen).pack(pady=[200, 0])
        Button(self.body_frame, text="Регистрация клиента", font=('Arial 12'), width=30, height=3, command=self.user_registered_screen).pack(pady=20)
        Button(self.body_frame, text="Вход для рабочего", font=('Arial 12'), width=30, height=3, command=self.user_login_screen).pack(pady=[0, 200])

    def login_default_screen(self, name_id):
        self.clear_body()

        self.login_body_frame = Frame(self.body_frame, name=name_id)
        self.login_body_frame.pack(anchor=CENTER)

        Button(self.head_frame, text='Назад', font=('Arial 10'), width=10, height=2, command=self.main_screen).pack(anchor=E, pady=[5, 0])

        Label(self.login_body_frame, text='Логин', font=('Arial 18')).grid(row=0, column=0, sticky=W, pady=[260, 0])
        Entry(self.login_body_frame, name='login', font=('Arial 20')).grid(row=1, column=0, pady=[0, 16])
        Label(self.login_body_frame, text='Пароль', font=('Arial 18')).grid(row=2, column=0, sticky=W)
        Entry(self.login_body_frame, name='password', font=('Arial 20'), show='•').grid(row=3, column=0)
        Button(self.login_body_frame, text='', font=('Arial 1'), width=22, height=16, command=self.hide_password).grid(row=3, column=1, padx=[10, 0])

    def user_login_screen(self):
        self.login_default_screen('user_login')

        Button(self.body_frame, text='Вход', font=('Arial 12'), width=10, height=2, command=self.user_authentication).pack(pady=[20, 260])

    def user_registered_screen(self):
        self.login_default_screen('registered')

        Label(self.login_body_frame, text='Повторите пароль', font=('Arial 18')).grid(row=4, column=0, sticky=W, pady=[16, 0])
        Entry(self.login_body_frame, name='repeat_password', font=('Arial 20'), show='•').grid(row=5, column=0)

        Button(self.body_frame, text='Регистрация', font=('Arial 12'), width=14, height=2, command=self.registred_user).pack(pady=[20, 260])

    def admin_login_screen(self):
        self.login_default_screen('admin_login')

        Button(self.body_frame, text='Вход', font=('Arial 12'), width=10, height=2).pack(pady=[20, 260])

    def hide_password(self):
        login_window = self.body_frame.children.get("admin_login") or self.body_frame.children.get("user_login") or self.body_frame.children.get("registered")
        for password_key in ["password", "repeat_password"]:
            password = login_window.children.get(password_key)
            if password:
                if password.cget('show') == '':
                    password.config(show="•")
                else:
                    password.config(show="")
            else:
                continue


    def user_authentication(self):
        get_value = self.body_frame.children.get("user_login")
        login_value = get_value.children.get("login").get()
        password_value = get_value.children.get("password").get()
        password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
        print(login_value, password_value)
        if mydb.search_user_for_login(login_value, password_value):
            print(login_value)
            self.request_screen(login_value, 'user')
        else:
            messagebox.showwarning(title='nini', message='неверный пароль или логин')
   
    def registred_user(self):
        get_value = self.body_frame.children.get("registered")
        login_value = get_value.children.get("login").get()
        password_value = get_value.children.get("password").get()
        repeat_password = get_value.children.get("repeat_password").get()
        if len(password_value) < 5:
            messagebox.showwarning(title='nini', message='пароль слишком короткий')
        else:
            if password_value != repeat_password:
                messagebox.showwarning(title='nini', message='пароли не совпадают')
            else:
                password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
                print(login_value, password_value)
                if not mydb.check_and_get_user(login_value):
                    mydb.insert_value(login_value, password_value)
                else:
                    messagebox.showwarning(title='nini', message='пользователь с таким логином есть')
            
    def admin_authentication(self):
        get_value = self.body_frame.children.get("admin_login")
        login_value = get_value.children.get("login").get()
        password_value = get_value.children.get("password").get()
        password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
        print(login_value, password_value)
        if mydb.search_admin_for_login(login_value, password_value):
            print(login_value)
            self.request_screen(login_value, 'admin')
        else:
            messagebox.showwarning(title='nini', message='неверный пароль или логин')


    def menu_exit_pro(self):
        self.main_menu.destroy()
        self.main_screen()

    def request_screen(self, login, status):
        self.clear_main()
        self.user_name = login

        self.main_menu = Menu()
        file_menu = Menu(tearoff=0)
        file_menu.add_command(label=self.user_name)
        file_menu.add_command(label="Выйти из профиля", command=self.menu_exit_pro)
        file_menu.add_separator()
        file_menu.add_command(label="Выйти из приложения", command=self.root.destroy)
        self.main_menu.add_cascade(label="Профиль", menu=file_menu)
        self.root.config(menu=self.main_menu)

        request_head_frame = Frame(self.head_frame)
        request_head_frame.pack(pady=25)
        Entry(request_head_frame, font=('Arial 18'), width=50).grid(row=0, column=0)
        Button(request_head_frame, text='поиск', font=('Arial 14'), width=10).grid(row=0, column=1)

        request_body_frame = Frame(self.body_frame)
        request_body_frame.pack(pady=100)
        if status == 'user':
            Button(request_body_frame, text='Подать заявку', font=('Arial 14'), width=20, height=2, command=self.add_request_screen).grid(row=0, column=0)
        Button(request_body_frame, text='Мои заявки', font=('Arial 14'), width=20, height=2).grid(row=1, column=0, pady=[20,0])

        statistic_frame = Frame(self.body_frame)
        statistic_frame.pack(pady=[250, 20])
        text = [f"количество выполненых заявок:   {5}", f'среднее время выполнения:   {1}', f'статистика по типам неисправнастям:   {4}']
        for i in text:
            Label(statistic_frame, text=i, font=('Arial 12') ).pack(anchor=W, pady=[0,10])

    def add_request_screen(self):
        window = Toplevel()
        window.title("заявка")
        window.geometry("1200x700")
        window.grab_set() 

        eq_box, ty_box = mydb.equipment_and_type_serch()
        

        add_request_body = Frame(window)
        add_request_body.pack(pady=50)

        titles = ["номер","клиент", "дата", "оборудование", "тип не исправности", "описание:" ]

        for count, title in enumerate(titles):
            Label(add_request_body, text=title, font=('Arial 12')).grid(row=count, column=0, sticky=W, pady=[0,10])
        
        id = Label(add_request_body, text=f"0000", font=('Arial 12')).grid(row=0, column=1, sticky=E, pady=[0,10])
        user = Label(add_request_body, text=self.user_name, font=('Arial 12')).grid(row=1, column=1, sticky=E, pady=[0,10])
        data = Label(add_request_body, text=today, font=('Arial 12')).grid(row=2, column=1, sticky=E, pady=[0,10])
        eq = ttk.Combobox(add_request_body, values=eq_box, font=('Arial 12'), state="readonly")
        eq.grid(row=3, column=1, sticky=E, pady=[0,10])
        ty = ttk.Combobox(add_request_body, values=ty_box, font=('Arial 12'), state="readonly")
        ty.grid(row=4, column=1, sticky=E, pady=[0,10])
        op = Text(add_request_body, font=('Arial 14'), height=10).grid(row=6, column=0, columnspan=2, sticky=E, pady=[0,10])
        Button(add_request_body, text='далее', font=('Arial 14'), width=16, height=3).grid(row=7, column=0)
        Button(add_request_body, text='назад', font=('Arial 14'), width=16, height=3, command=window.destroy).grid(row=7, column=1)

        print(eq.get())
        
        



    





    




    









    def run(self):
        self.root.mainloop()

start = App()
start.run()