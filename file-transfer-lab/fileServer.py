#!/usr/bin/env python3

import socket

#from fileClient import filename    #instead I need to send filename first through sendall

HOST = '127.0.0.1'# Standard loopback interface address (localhost)
PORT = 65432# Port to listen on (non-privileged ports are > 1023)


def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
	#		print(filename) #somehow wait to recieve filename before writing
	#		print(filename)
			#fileWriter = open(filename, 'wb')

	#		while True: #(i < !bytesInfile): #Somehow read until the end of the file
	#			#pass global bytesInFile
	#			data = conn.recv(1024)
	#			if not data:
	#				break
	#			conn.sendall(data)
	#			fileWriter.write(data)

	#		fileWriter.close()
	#		data = conn.recv(24)


			while True:
				data = conn.recv(1024)
				d = data.decode()

				if ".txt" in d: #First thing sent will always be the filename
					spl = d.split(",")
					biteSyze = spl[-1]
					filename = spl[0]
					print(filename)
					print(biteSyze)
					writeFile(filename,biteSyze)

				print(data)
				if not data:
					break
				conn.sendall(data)
			
			
if __name__ == '__main__':
    main()

			