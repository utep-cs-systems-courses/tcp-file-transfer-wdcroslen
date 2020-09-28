#!/usr/bin/env python3

import os,sys,socket
from stat import *

HOST = '127.0.0.1'# The server's hostname or IP address
PORT = 65432# The port used by the server



def getSize(filename):
    st = os.stat(filename)
    return st.st_size  #filesize in bytes


#TODO: Delete file?

def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		#ask for file
		#for now send as messages
		print("Hello User, type the name of your file you would like to send.")
		while True:
			filename = input("$ ")
			if filename == "exit":
				sys.exit(0)
			try:
				fs = open(filename, 'rb')
			except IOError:
				pass
				print("File not found, please try again.")
			else:
				s.sendall(filename.encode() + ("oof," + str(getSize(filename)) + "oof,").encode())
				#TODO replace the comma with a character that won't be in the file
				while True:
					data = fs.read(1024)
					s.sendall(data)
					if not data:
						break
				fs.close()
				print('Send complete.')


		#maybe from this side I can send an end of file char to signal file end
	#    s.sendall(b'Hello, world')
	#    data = s.recv(1024)

	print('Received', repr(data))


if __name__ == '__main__':
    main()

