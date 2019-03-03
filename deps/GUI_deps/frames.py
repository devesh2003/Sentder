from tkinter import *

class Window(Frame):
    def __init__(self, master=None, title="Sentder", size="400x400"):
        global window_title
        window_title = title
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry(size)
        self.init_window()

    def init_window(self):
        self.master.title(window_title)
        self.pack(fill=BOTH)
        self.create_window()

    def create_window(self):
        self.master.mainloop()

root = Tk()
app = Window(master=root,title="Test")
