#Basic Code to get up and Running
#This Setup is for a SERVER


import select
import socket
import sys
import datetime

#What does this do? Why won't it work on the bluebox if I use localhost?
host = ''
port = 50004 #Put Your Specific Port Here

if len(sys.argv) > 1:
    port = int(sys.argv[1])

backlog = 5
size = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#This releases the port immediately upon termination of the program
#It helps avoid the socket.error: [Errno 48] Address already in use
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host,port))

print 'Your server is running on Port: %s , Type to exit' % port
server.listen(backlog)

timeout = 10 #Remember the units are [Seconds]
#input is a list for the select mechanism. Remember sys.stdin isn't Widows compat
inputList = [server]
#Set yor flag to run the main loop
running = True

while running:
        inputSelected,outputSelected,exceptSelected = select.select(inputList,[],[],timeout)

        #Handle the timeout case, for example using a tick / timestamp
        #This will fire if nothing is returned to the inputSelected List
        if not inputSelected:
            print 'Server running at %s' % datetime.datetime.now()

        #For each item that is returned, it means an input needs handled
        for s in inputSelected:

            #This means that someone wants to connect if the server socket needs handled
            if s == server:
                client, address = server.accept()
                #Remember, we have to tell select to now also listen to the client 
                inputList.append(client)
                print 'Accepted connection from: ', address

            #The other initial input device being listened for is the keyboard
            #If the keyboard (or anything redirected to stdin) is used, handle that
            #Have to comment all stdin code out to get this to run with nohup?!
            ##elif (s.isatty() and s==sys.stdin):
                #Remember this won't work for windows
                ##junk = sys.stdin.readline()
                #Set flag to False to drop out of the loop
                ##running = False
                #print "Input: %s detected from stdin, Terminating." % junk.strip('\n')

            #otherwise you should be only handling client sockets
            elif s:
                #you should always get data from the client socket, wrapped in socket stuff
                #using recv you strip all the stuff away to get at the tasty data inside
                data = s.recv(size)
                print '%s: %s' % (s.getpeername(), data.strip('\n'))
                #if the data inside has content, then echo it
                if data:
                    for j in inputList:
                        if (j is not server )and (j is not sys.stdin):
                            j.send('%s' % data)
                #otherwise, the data inside was empty, ergo, close socket
                #don't forget to also remove it from the input list
                else:
                    s.close()
                    print 'Closed Connection'
                    inputList.remove(s)

#After dropping through the Loop, close the server socket
s.close()
