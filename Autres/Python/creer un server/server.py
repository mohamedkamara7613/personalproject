#coding:utf-8
#python 2.X

import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 8080 #port suppérieur a 1000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print("Listening on {}:{}\n:".format(bind_ip, bind_port))


def manage_client(client_socket):
	while True:
		request = client_socket.recv(1024)
		print("Received : {}".format(request))
		client_socket.send("ACCEPTED!\n:")


while True:
	client, addr = server.accept()
	print("accepted connection from {}:{} ".format(addr[0], addr[1]))
	manage_client = threading.Thread(target=manage_client, args=(client,))
	manage_client.start()