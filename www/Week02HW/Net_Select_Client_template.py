#Basic Code Setup for a non-blocking chat client
#based off of Instructor's recho_client.py example

import socket
import sys
import select
import datetime

host = ''
port = 50004 #Put your specific port here
size = 1024
username='Default'
username = raw_input("Username: ")


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
inputList=[client,sys.stdin]
Running = True
timeout = 10


while Running:
    inputSelected,outputSelected,exceptSelected = select.select(inputList,[],[],timeout)

    #Handle the timeout case, for example using a tick / timestamp
    #This fires if nothing is returned to the inputSelected List
    if not inputSelected:
        print 'Client running at %s' % datetime.datetime.now()

    #For each item that is returned, it means an input needs handled
    for k in inputSelected:

        #This means that there is message traffic from the server
        if k==client:
            data = client.recv(size)
            if data:
                print data.strip('\n')
            #in this case, a zero payload message was received (closed by remote)
            else:
                client.close()
                Running = False

        #Else you should only be handling the keyboard
        elif k==sys.stdin:
            data = sys.stdin.readline()
            client.send(('%s: %s') % (username,data))
        #otherwise nothing else should go on
        else:
            pass
