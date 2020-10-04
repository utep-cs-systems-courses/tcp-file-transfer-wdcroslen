#!/usr/bin/env python3

import os,sys,socket,re
from stat import *  #for byte size of file
sys.path.append("../lib")       # for params
import params

HOST = '127.0.0.1'# The server's hostname or IP address
PORT = 65432# The port used by the server



def getSize(filename):
	st = os.stat(filename)
	return st.st_size#filesize in bytes

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
	(('-s', '--server'), 'server', "127.0.0.1:50001"),
	(('-d', '--debug'), "debug", False), # boolean (set if present)
	(('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
#paramMap = params.parseParams(switchesVarDefaults)
#server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]
#
#

while True:
	print("Hello User, type the name of your file you would like to send.")
	fileName = input("$ ")
	if fileName == "exit":
		sys.exit(0)
	try:
		fs = open(fileName, 'rb')
		break
	except IOError:
		pass
		print("File not found, please try again.")
	
#    try:
#        fileName = input("Please enter the name of the file you'd like to send: ")
#        file = open(fileName, "rb")
#        break
#    except FileNotFoundError:
#        print("File does not exist, please enter another file name to try again")
			
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
	serverHost, serverPort = re.split(":", server)
	serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

fileContents = fs.read()

if len(fileContents) == 0:
    print("File is empty, exiting")
    sys.exit(1)

#s.sendall(filename.encode() + ("oof," + str(getSize(filename)) + "oof,").encode())
#print("sending fileName")

framedSend(s, fileName, fileContents, debug)







###############
#if usage:
#	params.usage()
#	
#try:
#	serverHost, serverPort = re.split(":", server)
#	print(serverPort)
#	serverPort = int(serverPort)
#except:
#	print("Can't parse server:port from '%s'" % server)
#	sys.exit(1)
#
#addrFamily = socket.AF_INET
#socktype = socket.SOCK_STREAM
#addrPort = (serverHost, serverPort)
#
#s = socket.socket(addrFamily, socktype)
#
#if s is None:
#	print('could not open socket')
#	sys.exit(1)
#
#s.connect(addrPort)
#
#
#
#
#def main():
##	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
##		s.connect((HOST, PORT))
#		#ask for file
#		#for now send as messages
#		print("Hello User, type the name of your file you would like to send.")
#		while True:
#			filename = input("$ ")
#			if filename == "exit":
#				sys.exit(0)
#			try:
#				fs = open(filename, 'rb')
#			except IOError:
#				pass
#				print("File not found, please try again.")
#			else:
#				s.sendall(filename.encode() + ("oof," + str(getSize(filename)) + "oof,").encode())
#				#TODO replace the comma with a character that won't be in the file
#				while True:
#					data = fs.read(1024)
#					s.sendall(data)
#					if not data:
#						break
#				fs.close()
#				print('Send complete.')
#
#
#	#	maybe from this side I can send an end of file char to signal file end
#	#    s.sendall(b'Hello, world')
#	#    data = s.recv(1024)
#
#		print('Received', repr(data))
#
#
#if __name__ == '__main__':
#	main()

