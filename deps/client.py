#Author : Devesh Shah

#######################################
#                                     #
#              SENTDER                #
#               v 1.0                 #
#                                     #
#######################################

import socket
from hashlib import md5
import struct
from time import sleep

import sys
sys.path.append("/Users/pathik/Desktop/Sentder/deps")
from interactive_interface import *

global _username_
global _passwd_
global _headers_
_headers_ = struct.pack('<BBBBHH',2,0,0,3,2,1)
_username_ = ""
_passwd_ = ""

def check_mail(s):
        global _headers_
        s.send(_headers_)
        sleep(1)
        s.send(("CheckMail").encode())
        mails_status = s.recv(10240)
        #print(str(mails_status))
        a,b,c,d,e,f,status = struct.unpack("<BBBBHHs",mails_status)
        if(status.decode() == "N"):
                print("No mails...")
        if(status.decode() == "M"):
                user_mails = s.recv(10240)
                num_mails = struct.unpack("<H",user_mails)
                print("Total %d mails in inbox"%(num_mails[0]))
                sleep(1)
                for i in range(0,int(num_mails[0])):
                        print("Mail number %d : "%(i+1))
                        nms = s.recv(10240)
                        new_mail_size = struct.unpack("<H",nms)
                        new_mail = s.recv(204800)
                        mail_raw = struct.unpack("<%ds"%(int(new_mail_size[0])),new_mail)
                        print("Mail : %s"%(mail_raw[0].decode("utf-8")))
                print("\n\nAll mails downloaded!")

def send_mail(s):
        global _headers_
        global _username_
        username = input("To : ")
        mail_body = input("Message : ")
        mail_size = len(mail_body)
        size_username = len(username)
        #print(_headers_)
        s.send(_headers_)
        s.send(("SendMail").encode())
        sleep(1)
        size_details_packet = struct.pack("<HH",size_username,mail_size)
        s.send(size_details_packet)
        sleep(2)
        mail_packet = struct.pack("<%ds%ds"%(size_username,mail_size),username.encode(),mail_body.encode())
        s.send(mail_packet)
        serv_confrim = s.recv(10240)
        if(serv_confrim.decode() == "Sent"):
                print("Message sent")
        else:
                print("Message Transfer Failed")

def mails(s):
        print("1) Check Inbox")
        print("2) Send mail")
        opt = input(">")
        if(int(opt) == 1):
                check_mail(s)
        if(int(opt) == 2):
                send_mail(s)

def get_details():
        global _username_
        global _passwd_
        username = str(input("Enter username : "))
        passwd_raw = str(input("Enter password : "))
        passwd = md5(passwd_raw.encode("utf-8")).hexdigest()
        _username_ = username
        _passwd_ = passwd

def register(s):
        get_details()
        global _username_
        global _passwd_
        global _headers_
        print(_headers_)
        s.send(_headers_)
        data_formatted = _username_ + ";" + _passwd_
        s.send(data_formatted.encode())
        resp = s.recv(15360)
        #print(str(resp))
        a,b,c,d,e,f,serv_resp = struct.unpack("<BBBBHH5s",resp)
        if(serv_resp.decode() == "ADDED"):
                print("[*] Registered! You may login")
        else:
                print("[*] Registration Failed...! Please try again")
                return
        login(s)

def login(s):
        global _username_
        global _passwd_
        global _headers_
        if(len(_username_) < 6 or len(_passwd_) < 6):
                get_details()
        s.send(_headers_)
        resp = s.recv(1024*20)
        a,b,c,d,e,f,serv_resp = struct.unpack("<BBBBHH12s",resp)
        if(serv_resp.decode() == "AUTHENTICATE"):
                size_username = len(_username_)
                size_passwd = len(_passwd_)
                size_details_packet = struct.pack("<HH",size_username,size_passwd)
                s.send(size_details_packet)
                sleep(2)
                details_packet = struct.pack("<%ds%ds"%(int(size_username),int(size_passwd)),_username_.encode("utf-8"),_passwd_.encode("utf-8"))
                s.send(details_packet)
                sleep(1)
                if(s.recv(1024).decode() == 'SUCCESS'):
                    print("Logged in!")
                    mails(s)
                else:
                    print("\n\nInvalid Username/Password")
                    sys.exit(0)

def get_option(s):
        print("1) Login")
        print("2) Register")
        print("3) Exit")
        opt = input("Select an option > ")
        if(int(opt) == 2):
                #print("Registering..")
                enc = ("R").encode("utf-8")
                reg_packet = struct.pack("<1s",enc)
                #print(str(reg_packet))
                s.send(reg_packet)
                register(s)
        if(int(opt) == 1):
                s.send("L".encode())
                login(s)

def connect():
        global _headers_
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[*] Connecting...")
        s.connect(("127.0.0.1",2003))
        s.send(_headers_)
        resp = s.recv(1024)
        a,b,c,d,e,f,serv_resp = struct.unpack("<BBBBHH4s",resp)
        #print(str(serv_resp))
        if(serv_resp.decode() == "TYPE"):
                get_option(s)

def main():
        connect()


if __name__ == '__main__':
        main()
