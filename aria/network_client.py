import os
import socket
import sys
import signal


def handler(signum, frame):
	pass


# establish connection to the game server
def connect(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	server_address = (str(host), int(port))
	sock.connect(server_address)
	return sock

	
# send a message and its length to the game server
# todo: might need a wrapper to handle when sendall hangs
# todo: handle login later - (login will have 3 fields)
def send_login(sock, cmd):
	
	try:
		method, name, clas = cmd.split()[:3]
	except:
		pass
		# dosomething

	stime = time.time()
	message = {
				"method":method,
				"name":name,
				"class":clas
			}	
	
	length = str(len(message))
	combined = length + '!' + message
	sock.sendall(combined.encode())


# send a message and its length to the game server
# todo: might need a wrapper to handle when sendall hangs
# todo: handle login later - (login will have 3 fields)
def send(sock, cmd):
	 try:
		method, arg = cmd.split()[:2]
	except:
		pass
		# dosomething

	stime = time.time()
	message = {
				"method":method,
				"arg":arg
			}	
	
	length = str(len(message))
	combined = length + '!' + message
	sock.sendall(combined.encode())




# recieve a message from the game server
def recv(sock):

	buf = ''
	while '!' not in buf:
		d = sock.recv(1)
		d = d.decode()
		buf += d

	length = buf[0:len(buf)-1]
	
	data = sock.recv(int(length))
	while(len(data) < int(length)):
		data += sock.recv(int(length))

	data = data.decode()
	return data


