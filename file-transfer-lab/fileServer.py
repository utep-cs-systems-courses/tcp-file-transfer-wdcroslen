#!/usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

from threading import Thread, Lock
lock = Lock()

HOST = '127.0.0.1'# Standard loopback interface address (localhost)
PORT = 65432# Port to listen on (non-privileged ports are > 1023)

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

def writeFile(filename, biteSyze, conn): #FIXME: second file writing does nothing 
	i = 0
	fileWriter = open(filename, 'wb')
	while (i < int(biteSyze)): #Somehow read until the end of the file
			data = conn.recv(1024)
			if not data:
				break
			conn.sendall(data)
			fileWriter.write(data)
			i += len(data)
			print(data)

	fileWriter.close()

	
	
	
	


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


class Server(Thread):
	def __init__(self, lsock):
		Thread.__init__(self)
		self.sock, self.addr = lsock
		
	def run(self):
		while True:
			from framedSock import framedSend, framedReceive

			print("new child process handling connection from", self.addr)
			payload = ""
			lock.acquire()
			#receive file name and contents
			fileName, fileContents = framedReceive(self.sock, debug)


			if debug: print("rec'd: ", payload)

			if payload is None:
				print("File contents were empty, exiting...")
				lock.release()
				sys.exit(1)

			#receive fileName
			fileName = fileName.decode()
			if fileName == "exit":
				lock.release()
				sys.exit(0)

			try:
				#write file to transfer dir
				if not os.path.isfile("./transfer/" + fileName):
					file = open("./transfer/" + fileName, 'w+b')
					file.write(fileContents)
					file.close()
					print("File:", fileName, "successfully accepted!")
					lock.release()
					sys.exit(0)
				else:
					print("File: ", fileName, "already exists.")
					lock.release()
					sys.exit(1)
					
			except FileNotFoundError:
				print("File Not Found")
				lock.release()
				sys.exit(1)
				
while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
			