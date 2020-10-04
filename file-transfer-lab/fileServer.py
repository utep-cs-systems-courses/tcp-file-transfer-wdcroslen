#!/usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

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
		#need to split better
#			print("its go time")
			data = conn.recv(1024)
			if not data:
#				fileWriter.write(("Done").encode())
				break
			conn.sendall(data)
			fileWriter.write(data)
			i += len(data)
			print(data)

	fileWriter.close()

def main():
#	
	lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
	bindAddr = ("127.0.0.1", listenPort)
	lsock.bind(bindAddr)
	lsock.listen(5)
	print("listening on:", bindAddr)

	while True:
		sock, addr = lsock.accept()

		from framedSock import framedSend, framedReceive
		
		if not os.fork():
			print("new child process handling connection from", addr)
			payload = ""
			try:
				fileName, fileContents = framedReceive(sock, debug)
			except:
				print("File transfer failed")
				sys.exit(1)

			if debug: print("rec'd: ", payload)

			if payload is None:
				print("File contents were empty, exiting...")
				sys.exit(1)

			fileName = fileName.decode()
			try:
				if not os.path.isfile("./transfer/" + fileName):
					file = open("./transfer/" + fileName, 'w+b')
					file.write(fileContents)
					file.close()
					print("File", fileName, "successfully accepted!")
					sys.exit(0)
				else:
					print("File: ", fileName, "already exists.")
					sys.exit(1)
			except FileNotFoundError:
				print("File Not Found")
				sys.exit(1)
				
#			while True:
#					data = sock.recv(1024)
#					d = data.decode()
#					spl = d.split("oof,")
#					print(spl)
#					biteSyze = spl[1] #byteSize
#					filename = spl[0]
##					
##					payload = framedReceive(sock, debug)
##					writeFile(filename,biteSyze,sock)
#					
#		while True:
#			sock, addr = lsock.accept()
#
#			if not os.fork():
#				print("connection rec'd from", addr)
				# sys.exit(1)

				

				
	#        while True:
#            payload = framedReceive(sock, debug)
#            if debug: print("rec'd: ", payload)
#            if not payload:
#                if debug: print("child exiting")
#                sys.exit(0)
#            payload += b"!"             # make emphatic!
#            framedSend(sock, payload, debug)


#	
#	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#		s.bind((HOST, PORT))
#		s.listen()
#		
#		
#		conn, addr = s.accept()
#		with conn:
#			print('Connected by', addr)
#			while True:
#				data = conn.recv(1024)
#				d = data.decode()
#				
#				spl = d.split("oof,")
#				print(spl)
#				biteSyze = spl[1] #byteSize
#				filename = spl[0]
#				
#				writeFile(filename,biteSyze,conn)
#
#				if not data:
#					break
#				conn.sendall(data)
			
			
			
##! /usr/bin/env python3

#import sys
#sys.path.append("../lib")       # for params
#import re, socket, params, os
#
#switchesVarDefaults = (
#    (('-l', '--listenPort') ,'listenPort', 50001),
#    (('-d', '--debug'), "debug", False), # boolean (set if present)
#    (('-?', '--usage'), "usage", False), # boolean (set if present)
#    )
#
#progname = "echoserver"
#paramMap = params.parseParams(switchesVarDefaults)
#
#debug, listenPort = paramMap['debug'], paramMap['listenPort']
#
#if paramMap['usage']:
#    params.usage()
#
#lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
#bindAddr = ("127.0.0.1", listenPort)
#lsock.bind(bindAddr)
#lsock.listen(5)
#print("listening on:", bindAddr)
#
#while True:
#    sock, addr = lsock.accept()
#
#    from framedSock import framedSend, framedReceive
#
#    if not os.fork():
#        print("new child process handling connection from", addr)
#        while True:
#            payload = framedReceive(sock, debug)
#            if debug: print("rec'd: ", payload)
#            if not payload:
#                if debug: print("child exiting")
#                sys.exit(0)
#            payload += b"!"             # make emphatic!
#            framedSend(sock, payload, debug)

if __name__ == '__main__':
    main()

			