"""
Modifed from echo_server_select.py
"""

import select
import socket
import time
import datetime
import sys

host = ''
port = 50004 #new port than other samples, all can run on same server

#Run on other than default port if new port number exists as first argument
if len(sys.argv) > 1:
    port = int(sys.argv[1])

backlog = 5
size = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Release port when scriptexits and avoid socket error
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

server.bind((host,port))

print 'Chat Server listening on port %s, to exit type [Enter]' % port
server.listen(backlog)

timeout = 10 #[Seconds]
input = [server, sys.stdin] #that's a list with the server socket and keyboard
running = True

while running:
    inputGo, outputGo, exceptGo = select.select(input,[],[],timeout)

    #timeout
    if not inputGo:
        print 'Chat Server running at %s' % datetime.datetime.now()

    for s in inputGo:
        if s == server:
            #this is the server socket
            client, address = server.accept()
            input.append(client)
            print 'User joined from %s' % address[0]
            
        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            running = False
            print 'Input %s from stdin, exiting.' % junk.strip('\n')

        elif s:
            #we got a live one (client that is)
            recdata = s.recv(size)
            print '%s' % recdata.strip('\n')
            if recdata:
                #send to all in input list
                print input
                for x in input:
                    if x is type(socket):
                        print '%s sent to %s' % (recdata, x)
                        x.send('%s' % recdata) #already stripped recdata above
            else:
                print 'A User has left. Connection closed.'
                s.close()
                input.remove(s)

s.close() #close the server socket
                
            
