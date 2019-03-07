from tkinter import *

class Window(Frame):
    def __init__(self, master=None, title="Sentder", size="400x400", icon=None):
        global window_title
        window_title = title
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry(size)
        Tk.iconbitmap(self.master, default=icon)
        self.init_window()

    def init_window(self):
        self.master.title(window_title)
        self.pack(fill=BOTH)
        self.create_window()

    def create_window(self):
        self.master.mainloop()
