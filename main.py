# #https://lenta.ru/news/2017/01/19/avalanche30/
# #https://www.gazeta.ru/politics/2017/01/19_a_10481981.shtml#page1
# #http://www.rbc.ru/politics/19/01/2017/58806cec9a7947114330fbbf
from tkinter import *
from tkinter.ttk import *
from reader import newsParser as nP
from tkinter import messagebox


class MainWindow(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.link = StringVar()
        self.text = None
        self.btn_img = PhotoImage(file='get_app.png')
        self.master.title('Читалка новостей')
        self.master.minsize(250, 500)
        self.master.resizable(height=False, width=False)
        self.pack()
        self.make_search_frame()
        self.make_text_frame()

    def make_search_frame(self):
        search_window = Frame(self)
        Label(search_window, text='Ссылка на новость', font=10).pack(side=LEFT, anchor=W)
        Entry(search_window, width=45, font=10, textvariable=self.link).pack(padx=15, side=LEFT, anchor=CENTER)
        Button(search_window, text='Загрузить', image=self.btn_img, command=self.get_link).pack()
        search_window.pack(side=TOP, pady=5)

    def make_text_frame(self):
        text_window = Frame(self)
        #Scrollbar(text_window, orient=VERTICAL).pack(side=RIGHT, fill=Y, expand=YES)
        self.text = Text(text_window, width=80, height=30)
        self.text.pack(side=TOP)
        text_window.pack()

    def get_link(self):
        if self.link.get():
            news = nP.NewsParser(self.link.get())
            news.start()
            with open(news.path, encoding='utf-8') as file:
                for line in file:
                    self.text.insert(END, line)
        else:
            messagebox.showwarning('Ошибка', 'Ссылка не обнаружена!')

root = Tk()
MainWindow(root).mainloop()
