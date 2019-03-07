from tkinter import *
from server import validate
from deps import hash
from deps.GUI_deps import frames

def login(username,passwd):
    passwd = hash.md5_hash(passwd)
    if(validate(username,passwd)):
        print("User verified")
    else:
        print("User not in DB")

class Window(Frame):
    global x_coords_usr,y_coord_usr,button_coord
    x_coords_usr = 50
    y_coord_usr = 100
    button_coord = [12,23]
    button_coord[0] = x_coords_usr + 150
    button_coord[1] = y_coord_usr + 180

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Sentder")
        self.pack(fill=BOTH, expand=1)
        #btn = Button(self,text="Button 1").place(x=50,y=100)
        self.init_fields()

    def init_fields(self):
        title_label = Label(self, text="Sentder", font=("algerian",30,"bold")).pack()
        usrname_label = Label(self, text="Enter your username :",font=("Arial",13,"bold")).place(x=x_coords_usr,y=y_coord_usr)
        passwd_label = Label(self, text="Enter your password :", font=("Arial",13,"bold")).place(x=x_coords_usr,y=(y_coord_usr+100))

        global usrname,passwd
        usrname = StringVar()
        passwd = StringVar()
        username_field = Entry(self, textvariable=usrname, width=30).place(x=(x_coords_usr+220),y=y_coord_usr+4)
        passwd_field = Entry(self, textvariable=passwd, width=30).place(x=(x_coords_usr+220),y=(y_coord_usr+104))
        self.init_buttons()

    def init_buttons(self):
        login_button = Button(text="Login", command=lambda: login(usrname.get(),passwd.get()), width=18).place(x=button_coord[0],y=button_coord[1])

        self.init_menu()

    def init_menu(self):
        master_menu = Menu(self.master)
        self.master.config(menu=master_menu)
        file_menu = Menu(master_menu)
        file_menu.add_command(label='Test')
        master_menu.add_cascade(label='Test Menu', menu=file_menu)

def main():
    root = Tk()
    root.geometry("580x400")
    app = Window(root)
    Tk.iconbitmap(root, default="C:/Users/pathik/Desktop/Sentder/deps/icon.ico")
    root.mainloop()

if __name__ == '__main__':
    main()

#root = Tk()
#frames.Window(master=root,title="Module",size="580x400", icon="C:/Users/pathik/Desktop/Sentder/deps/icon.ico")
