import os
from threading import Thread
import sys
from time import sleep

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
			file = open('creds.bin','ra')
			entries = file.read()
			for entry in entries:
				details = entry.strip('!').split(';')
				

def clear_database():
	pass

def clear_mails():
	pass
