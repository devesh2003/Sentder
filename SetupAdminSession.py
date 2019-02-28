import socket
import struct
from admin_actions import *
from hashlib import sha1

global _headers_
keyword = "deveshbaapo"
_headers_ = struct.pack("<BBBBHH",2,0,0,3,2,1)
global session_cookie_packet
session_cookie = sha1(keyword.encode("utf-8")).hexdigest()
session_cookie_packet = struct.pack("<%ds"%(len(session_cookie)),str(session_cookie).encode())


def verify_session(s):
    try:
        s.send("VERIFY_SESSION".encode())
        sleep(2)
        
    except Exception as e:
        #raise
        print("[*] Error : %s In verifying admin session"%(str(e)))


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
    s.send(menu.encode())
    sleep(2)
    data = s.recv(1024)
    a,b,c,d,e,f,serv_resp = struct.unpack("<BBBBHHH",data)
    if(serv_resp == 1):
        verify_session(s)
        send_users(s)
    elif(serv_resp == 2):
        pass
    elif(serv_resp == 3):
        pass
    elif(serv_resp == 4):
        pass
