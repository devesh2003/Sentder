import socket
import struct
from time import sleep

def get_input(s,question):
    #s : socket Connection
    #question : question for the input
    try:
        s.send(str(question).encode())
        s.sleep(1)
        answer = s.recv(1024).decode()
        return answer
    except:
        return 0

def send_input(s):
    #s : socket TCP connection
    #answer : input
    ques = s.recv(1024).decode()
    answer = input(ques)
    s.send(anwer.ecnode())
    sleep(1)
