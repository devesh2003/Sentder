import socket
import struct
from admin_actions import *
from hashlib import sha1
from interactive_interface import *
from server import remove_entry

global _headers_
keyword = "deveshbaapo"
_headers_ = struct.pack("<BBBBHH",2,0,0,3,2,1)
global session_cookie_packet
session_cookie = sha1(keyword.encode("utf-8")).hexdigest()
session_cookie_packet = struct.pack("<%ds"%(len(session_cookie)),str(session_cookie).encode())

def verify_headers(a,b,c,d,e,f):
    if(a == 2 and f == 1 and e == 2 and b == 0):
        return True
    else:
        return False

def verify_session(s):
    global session_cookie
    try:
        s.send("VERIFY_SESSION".encode())
        sleep(2)
        data = s.recv(10240)
        a,b,c,d,e,f,cookie = struct.unpack("<BBHHHH%ds"%(len(session_cookie)),data)
        if(verify_headers(a,b,c,d,e,f) == True and cookie == session_cookie):
            pass
        else:
            #Terminate session
            pass
            return
    except Exception as e:
        #raise
        print("[*] Error : %s In verifying admin session"%(str(e)))

def check_username(usrname):
    pass

def remove_user(s,username="null"):
    if(username == "null"):
        username = get_input(s,"Enter Username : ")
    if(check_username(username)):
        s.send('OK'.encode())
        remove_entry(username)
    else:
        s.send('ERROR'.encode())
        username = get_input(s,"Invalid Username Please enter a valid username \n Username : ")
        remove_user(s,username)

#BETA (Not Funtional)
def send_menu(s):
    global _headers_
    global session_cookie
    admin_packet = _headers_ + session_cookie_packet
    s.send(admin_packet)
    menu = "Welcome to Sentder Admin Interface"
    menu += "1) Get a list of all users"
    menu += "2) Delete a user"
    menu += "3) Reboot the server"
    menu += "4) FACTORY RESET (Caution : This Will Wipe The Whole Server)"
    serv_resp = get_input(s,menu)
    #s.send(menu.encode())
    #sleep(2)
    #data = s.recv(1024)
    #a,b,c,d,e,f,serv_resp = struct.unpack("<BBBBHHH",data)
    if(serv_resp == 1):
        verify_session(s)
        send_users(s)
    elif(serv_resp == 2):
        verify_session(s)
        remove_user(s)
        pass
    elif(serv_resp == 3):
        verify_session(s)
        pass
    elif(serv_resp == 4):
        verify_session(s)
        pass
