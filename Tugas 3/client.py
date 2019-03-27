from socket import *
import socket
import threading
from ast import literal_eval
import glob

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9000
sock.connect((host, port))
name = raw_input('your name: ')

while True:
	command = raw_input('your command: ')
	if command[0] == "exit":
		break
	sock.send(command)
	command = command.split(" ")
	
	print '\n----------'
	files = ''
	if command[0] == 'show':
		print "Menunjukkan files"
		print '----------'
		data = sock.recv(1024)
		files = literal_eval(data)
		for filename in files:
			print filename
			
	elif command[0] == 'download':

		if len(command) == 2:
			sock.settimeout(1)
			print "Mengunduh files"
			print '----------'
			real = command[1].split("/")
			filename = name+'_'+str(real[-1])
			file = open(filename, 'wb')
			print "Receiving... ", filename

			while True:

				try:
					data = sock.recv(32)
					file.write(data)
					
				except timeout:

					break

			file.close()
			print "Selesai menerima ", filename
			
		else:

			print "syntax error"

	elif command[0] == 'upload':

		if len(command) == 2:
			files = glob.glob("*")
			print "Mengunggah files"
			print '----------'
			filename = command[1]

			if filename in files:

				with open(filename, 'rb') as file:
					print 'Mengirim ke server... '

					while True:
						print 'Sending... {} to server' . format(filename)
						bytes = file.read(1024)

						if not bytes:

							break
						sock.send(bytes)
					file.close()
				print "Selesai Mengirim", filename

			else:
				print "file tidak ditemukan"

		else:
			print "error"
			
	else:
		print "Perintah tidak ditemukan"
	print '----------\n'

sock.close()
