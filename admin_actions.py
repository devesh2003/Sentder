import os
from threading import Thread
import sys
from time import sleep
import socket

def send_users(s):
	file = open("creds.bin",'r')
	data = file.read()
	entries = data.split('!')
	#num_entries = len(entries) - 1
	user_menu = ""
	usernames = {}
	count = 1
	for entry in entries:
		details = entry.split(';')
		username = details[0]
		if(username == ""):
			continue
		user_menu += "%d) %s"%(count,username)
		usernames[count] = username
		count += 1
	file.close()
	s.send(user_menu.encode())

def check_username(usr):
	file = open("creds.bin",'r')
	entries = file.read().split("!")
	print("Total %d Entries"%(len(entries)))
	for entry in entries:
		data = entry.split(";")
		username = data[0]
		if(username == usr):
			return True
			file.close()
	return False
	file.close()

def suspend_acc():
	print("Suspend Account Process Started...")
	usrname = input("Enter username : ")
	if(check_username(usrname)):
		opt = input("Are you sure you want to Suspend %s ? (y/n)"%(usrname))
		if(opt == 'y' or opt == 'yes'):
			file = open('creds.bin','r')
			file2 = open('creds.bin.tmp','w')
			entries = file.read().split('!')
			for entry in entries:
				details = entry.split(';')
				user = details[0]
				if(user == usrname):
					continue
				data += entry + '!'
			file2.write(data)
			file2.close()
			file.close()
			os.remove('creds.bin')
			os.rename("creds.bin.tmp","creds.bin")


def clear_database():
	pass

def clear_mails():
	pass
