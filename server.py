#Author : Devesh Shah

#######################################
#									  #					
#				SENTDER 			  # 						
#				 v 1.0				  #
#									  #					
#######################################

import socket
import struct
from hashlib import md5
import os
from threading import Thread
from time import sleep

global _username_ 
global _passwd_ 
global _headers_
_headers_ = struct.pack("<BBBBHH",2,0,0,3,2,1)

def register(client):
	global _headers_
	try:
		data = client.recv(10240)
		headers = struct.unpack("<BBBBHH",data)
		if(headers[0] == 2 and headers[2] == 0 and headers[4] == 2):
			details = client.recv(10240).decode()
			username,passwd = details.split(";")
			#passwd = md5(passwd_raw.encode("utf-8")).hexdigest()
			formatted_data = username + ';' + passwd + '!'
			#file_name = md5(username.encode("utf-8")).hexdigest() + '.bin'
			main_file = open("creds.bin",'a')
			main_file.write(formatted_data)
			main_file.close()
			client.send(_headers_ + ("ADDED").encode())
	except Exception as e:
		print("Error in register : " + e)

def check_req(client):
	global _headers_
	try:
		data = client.recv(10240)
		print(str(len(data)) + str(data))
		headers = struct.unpack("<BBBBHH",data)
		if(headers[0] == 2 and headers[2] == 0 and headers[4] == 2):
			client.send(_headers_ + ("TYPE").encode())
			data = client.recv(10240)
			print(str(data))
			req_type = struct.unpack("<1s",data)
			return req_type[0].decode()
	except Exception as e:
		print("Error in check_req : " + str(e))

def validate(user,passwd):
	global _username_ 
	global _passwd_ 
	try:
		file = open("creds.bin",'r')
		data = file.read()
		entries = data.split('!')
		for entry in entries:
			details = entry.split(";")
			username = details[0]
			if(username == user):
				if(passwd == details[1]):
					file.close()
					return True
		file.close()
		return False

	except Exception as c:
		print("Error : " + c)
		file.close()
		return False

def verify(client):
	global _username_ 
	global _passwd_ 
	global _headers_
	try:
		try:
			print("In verify")
			data = client.recv(10240)
			headers = struct.unpack("<BBBBHH",data)
			if(headers[0] == 2 and headers[2] == 0 and headers[4] == 2):
				print("Verified headers")
				client.send(_headers_ + ("AUTHENTICATE").encode())
				print("sent mail_packet")
				size = client.recv(10240)
				print("Size received")
				size_details = struct.unpack("<HH",size)
				print("unpacked size")
				size_username = int(size_details[0])
				size_passwd = int(size_details[1])
				print(str(size_username))
				#sleep(2)
				so = 1024*80
				details = client.recv(102400)
				print("details received")
				client_details = struct.unpack("%ds%ds"%(size_username,size_passwd),details)
				print("Details unpacked")
				username = str(client_details[0].decode())
				passwd = str(client_details[1].decode())
				print("Values assigned ")
				print("username : %s passwd : %s"%(username,passwd))
				if(validate(username,passwd)):
					print("validated")
					_username_ = username
					_passwd_ = passwd
					return True
				else:
					#print("Error : ")
					return False
			else:
				#client.send(("Invalid code").encode())
				print("Error : ")
				client.close()
		except Exception as a:
			print("Error in verify : " + a)
			#client.send(("Invalid code").encode())
			client.close()
	except Exception as b:
		print("Error in verify_main : " + b)

def create_container(name):
	file = open(name,'w')
	file.close()

def send_mail(s):
	try:
		data = s.recv(1024)
		print(data)
		size_username,size_mail_body = struct.unpack("<HH",data)
		mail = s.recv(20480)
		username,mail_content = struct.unpack("<%ds%ds"%(size_username,size_mail_body),mail)
		username = username.decode()
		mail_content = mail_content.decode()
		print("Mail to : " + str(username))
		os.chdir("Mails")
		file_name = md5(username.encode("utf-8")).hexdigest() + ".bin"
		if(os.path.isfile(file_name) != True):
			create_container(file_name)
		file = open(file_name,'a')
		data_formatted = mail_content + ";"
		file.write(data_formatted)
		file.close()
		s.send("Sent".encode())
	except Exception as e:
		print("Error in send mail : " + str(e))

def check_mail(username,client):
	global _username_ 
	global _passwd_ 
	global _headers_
	os.getcwd()
	os.chdir("Mails")
	while True:
		try:
			file_name = md5(_username_.encode("utf-8")).hexdigest() + '.bin'
			if(os.path.isfile(file_name) != True):
				create_container(file_name)
			file = open(file_name , 'r')
			try:
				data = file.read()
				total_mails = data.split(';')
				user_mails = str(len(total_mails) - 1)
				print("Total mails for " + _username_ + " : " + user_mails)
				if(len(total_mails) == 0 or len(total_mails) == 1):
					msg = "N"
					client.send(_headers_ + msg.encode())
					sleep(2)
					return
					#sleep(3)
				client.send(_headers_ + ("M").encode())
				sleep(2)
				num_mails_packet = struct.pack("<H",int(user_mails))
				client.send(num_mails_packet)
				sleep(1)
				for mail in total_mails:
					mail_length = len(mail)
					mail_length_packet = struct.pack("<H",mail_length)
					client.send(mail_length_packet)
					sleep(2)
					mail_packet = struct.pack("%ds"%(int(mail_length)), mail.encode("utf-8"))
					client.send(mail_packet)
					sleep(2)
					print("Mail sent to client")
					#sleep(3)
				client.close()
			except Exception as e:
				#No mail
				print("Error in check mail : " + str(e))

		except Exception as e:
			print("Error in check_mail : " + e)
		file.close()


#Obsolete function
def setup_mails():
	try:
		if(os.path.isfile("mails.bin") != True):
			file = open("mails.bin",'wr')
		else:
			file = open("mails.bin",'ar')

		total_mails = (file.read().split('!')) - 1
		print("[*] Mails setup complete.")

	except Exception as e:
		print("[*] Mails setup failed...")
		print("Error : " + e)
	file.close()

def opt_mail(s):
	# 1 - Check mail
	#2 - Send mail
	global _headers_
	#try:
	data = s.recv(1024)
		#print(str(data) + " in opt")
	headers = struct.unpack("<BBBBHH",data)
		#print("unpacked")
	if(headers[0] == 2 and headers[2] == 0 and headers[4] == 2):
			#print("headers Verified")
		type_mail = s.recv(10240)
			#print('req received')
			#print(str(type_mail))
		if(type_mail.decode() == "SendMail"):
			print("Sending...")
			return True
		if(type_mail.decode() == "CheckMail"):
			return False
	#except Exception as e:
		#print('Error in opt mail : ' + str(e))

def client_hander(client):
	global _username_
	global _passwd_
	try:
		if(str(check_req(client)) == 'R'):
			register(client)
		if(verify(client)):
			print("User logged in")
			if(opt_mail(client) != True):
				print("Checking Mail")
				check_mail(_username_,client)
			else:
				print("Sending mail")
				send_mail(client)
				#check_mail(_username_,client)
		else:
			#client.send(("Invalid details").encode())
			print("[*] Error : Invalid details")
			client.close()
			#break
	except Exception as ee:
			pass
			#print("Error : " + str(ee))
			client.close()


def start_server():
	global _username_ 
	global _passwd_ 
	#setup_mails()
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(("127.0.0.1",2003))
	s.listen(6)

	while True:
		try:
			client,addr = s.accept()
			print("[*] Connection from " + str(addr[0]))
			client_thread = Thread(target=client_hander,args=(client,))
			client_thread.start()
			#client_hander(client)
		except Exception as ee:
			pass
			#print("Error : " + str(ee))
			s.close()

def main():
	start_server()

if __name__ == '__main__':
	main()
