from tkinter import *
import os

root = Tk()
root.title("Sentder")
root.geometry("550x500+0+10")

title = Label(root,text="Welcome To Sentder",font=("algerian",30,"bold")).pack()
usr_label = Label(root,text="Enter your usrname : ",font=("arial",10,"bold")).place(x=50,y=100)
username = StringVar()
usr_field = Entry(root,textvariable=username,width=30).place(x=210,y=100)

passwd = StringVar()
pass_label = Label(text="Enter password : ",font=("Arial",10,"bold")).place(x=50,y=200)
pass_field = Entry(root,textvariable=passwd,width=30).place(x=210,y=200)

def test():
    if(username.get() == "devesh2003" and passwd.get() == "deveshisgreat"):
        print("[*] Logged in!")
        root.destroy()
        root2 = Tk()
        root2.title("Admin Interface")
        root2.geometry("640x640+0+0")
        title = Label(root2,text="Control Panel",font=("Arial",30,"bold")).pack()
    else:
        root.destroy()
        root3 = Tk()
        root3.title("Access Denied")
        root3.geometry("400x200+0+0")
        title = Label(root3,text="Access Denied",font=("Arial",30,"bold")).pack()

login_button = Button(text="Login",command=test).place(x=200,y=250)

#imgicon = PhotoImage(file='icon.jpg')
#root.tk.call('wm', 'iconphoto', root._w, imgicon)
root.mainloop()
