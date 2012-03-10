# Thirty Minute Web Server originally by W. Fitzpatrick (rafial@well.com)
#
# Modified by Benjamin Bloss for Internet Programming in Python
# Further modified to return ISS location using web_api.py written by Benjamin Bloss
#
# updated for UW Internet Programming in Python, by Brian Dorsey
# updated by Jon Jacky: in defaults, replace '127.0.0.1' with ''
#  to allow connection from other hosts besides localhost
#

import os, socket, sys, calendar, datetime
from web_api import *

defaults = ['0.0.0.0', '8087']  # '127.0.0.1' here limits connections to localhost
mime_types = {'.jpg' : 'image/jpg', 
             '.gif' : 'image/gif', 
             '.png' : 'image/png',
             '.html' : 'text/html', 
             '.pdf' : 'application/pdf',
              '.py' : 'text/x-python'}
response = {}

response[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

response[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

response[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

DIRECTORY_LISTING =\
"""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""

DIRECTORY_LINE = '<a href="%s">%s</a><br>'

#############################################################
#Inserted by Benjamin Bloss
#
#ISS_PAGE Variables: <Latitude>,<Longitude><NextRise><NextDuration>
ISS_PAGE=\
"""<html>
<head><title> ISS Location and Pass Data for Seattle, Washington Waterfront</title></head>
<body> <CENTER>
<h2> Current Location of the International Space Station:</h2>
<table border cellpadding=5><tr><td>LATITUDE</td><td>LONGITUDE</td></tr>
<tr><td>%s</td><td>%s</td></tr></table>
<br>
<h2> Next Pass Data for Seattle Washington Waterfront Public Pier </h2>
<table border cellpadding=5><tr><td>Risetime</td><td>Duration</td></tr>
<tr><td>%s</td><td>%s</td></tr></table>
<h3>This page uses the open-notify api available at <a href=http://open-notify.org/> open-notify.org</a> 
<br>Programmed by Benjamin Bloss
</body>
</html>
"""



#CAL_PAGE Variables: <Title>,<Refresh>,<Date-Time>,<Calendar / Body>
CAL_PAGE=\
"""<html>
<head><title>%s</title><meta http-equiv="Refresh" content="%s"></head>
<body><CENTER>
<h2>%s</h2><br><br>
<pre>%s</pre></CENTER>
</body>
</html>
"""

def GenCalHTML(year):
    cal=calendar.HTMLCalendar(calendar.SUNDAY)
    return cal.formatyear(year, 3)




#
#############################################################

def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ##################Ran into problems, added our favorite fragment of code:
    # Release listener socket immediately when program exits, 
    # avoid socket.error: [Errno 48] Address already in use
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    s.listen(1)
    return s

def listen(s):
    connection, client = s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method = None
    while True:
        line = stream.readline()
        print line
        if not line.strip(): 
            break
        elif not method: 
            method, uri, protocol = line.split()
    return uri

def list_directory(uri):
    entries = os.listdir('.' + uri)
    entries.sort()
    return DIRECTORY_LISTING % (uri, uri, '\n'.join(
        [DIRECTORY_LINE % (e, e) for e in entries]))

def get_file(path):
    f = open(path)
    try: 
        return f.read()
    finally: 
        f.close()

def get_content(uri):
    print 'fetching:', uri
    try:
        path = '.' + uri
        if (path == './date.html') or (path == './time.html'):
            returnString = CAL_PAGE % ("Time Page",
                                       15,
                                       datetime.datetime.now(),
                                       GenCalHTML(datetime.datetime.now().year))
            return (200, mime_types['.html'], returnString) 
            
        elif (path == './iss.html'):
	    #Can't call get ISS position as two calls, one for LAT then LONG, must get together
	    #The station is travelling so fast that successive calls would result in a position
	    #that was never on the ISS path
	    (LAT,LON)=getISSPosition()
	    ISS = getISSPasses() #Default for Seattle
	    returnString = ISS_PAGE % (LAT, LON, ISS.niceRise(), ISS.niceDuration())
	    return (200, mime_types['.html'], returnString)
	    
        elif os.path.isfile(path):
            return (200, get_mime(uri), get_file(path))
        elif os.path.isdir(path):
            if(uri.endswith('/')):
                return (200, 'text/html', list_directory(uri))
            else:
                return (301, uri + '/')
        else: return (404, uri)
    except IOError, e:
        return (404, e)

def get_mime(uri):
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain')

def send_response(stream, content):
    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            stream = listen (server)
            send_response(stream, get_content(get_request(stream)))
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()

