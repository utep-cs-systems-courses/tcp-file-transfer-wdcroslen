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

while True:
	print("Hello User, type the name of your file you would like to send.")
	fileName = input("$ ")
	if fileName == "exit":
		break
#		sys.exit(0)
	try:
		fs = open(fileName, 'rb')
		break
	except IOError:
		pass
		print("File not found, please try again.")

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

framedSend(s, fileName, fileContents, debug)


