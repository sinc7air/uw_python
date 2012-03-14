#Basic Code Setup for a blocking chat client
#based off of Instructor's recho_client.py example

import socket
import sys

host = ''
port = 50004 #Put your specific port here
size = 1024

#if one option is included it is the host
#if a second argument is included it is the port number
nargs = len(sys.argv)
if nargs > 1:
    host =  sys.argv[1]
if nargs > 2:
    port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Release listener socket immediately when program exits, 
# avoid socket.error: [Errno 48] Address already in use
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client.connect((host,port))
print 'Connection accepted by (%s,%s)' % (host, port)
while True:
    #raw input prevents python language from being run
    msg = raw_input('Prompt:\> ')
    if msg:
        client.send(msg)
        data = client.recv(size)
        print data
    else:       #Server sent an empty payload, close connection
        client.close()
        break   #gracefully exit the loop

    
