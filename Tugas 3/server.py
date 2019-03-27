from socket import *
import socket
from threading import Thread
import glob


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((socket.gethostname(), 9000))
sock.listen(1)


def sendFiles(conn, name, addr):
	files = glob.glob("*")
	ip, port = addr
	try:
		with open(name, 'rb') as file:
			print 'Mengirim... ', addr
			while True:
				print 'Mengirim... {} to {}' . format(name, str(port))
				bytes = file.read(1024)
				if not bytes:
					break
				conn.send(bytes)
			file.close()
	except IOError:
		print "File tidak ditemukan"


def downloadFiles(addr, name):

	ip, port = addr
	file = open(str(port)+'_'+name, 'wb')
	print "Menerima... ", name
	sock.settimeout(2)

	while True:
		data = sock.recv(32)
		if not data:
			break
		file.write(data)
	file.close()
	print "Selesai menerima ", name

class ProcessTheClient(Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(1024)
			ip, port = self.address
			data = str(data).split(' ')
			print "{} Dari client {}".format(data[0], str(port))

			if data[0] == "show":
				files = glob.glob("*")
				self.connection.send(str(files))

			elif data[0] == 'download':
				if len(data) == 2:
					filename = data[1]
					sendFiles(self.connection, filename, self.address)
				else:
					print "error"

			elif data[0] == 'upload':
				if len(data) == 2:
					filename = data[1]
					downloadFiles(self.address, filename)
					print 'files'
				else:
					print "error"

			else:
				self.connection.send('error')

def server():
	while True:
		print "waiting for request"
		conn, addr = sock.accept()
		clt = ProcessTheClient(conn, addr)
		clt.start()
		
server()
