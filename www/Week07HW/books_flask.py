"""
Based on echo_flask.py from Internet Programming in Python (Jacky)

Written by B. Bloss

Displays an index page that displays a list of books and links to detail sub pages.
"""

from flask import Flask, request
from bookdb import * #This level of namespace pollution is acceptable for a small assigment

##Do not need a template, as Flask will wrapper our string in HTML

app = Flask(__name__)

app.debug = True #This is a class assignment - remove for production
Shelve=BookDB()

#View Functions

@app.route('/index.html' or '/books.html')
def bookIndex():
  bookshelve_body="<h2>bbloss' Index of Python Books from Class: </h2><br><table border cellpadding=5><tr><td><h3>Books</h3>"
  for record in Shelve.titles():
    bookshelve_body='</td></tr><tr><td>'.join([bookshelve_body,'<a href=%s/detail.html>%s</a>' % (record['id'],record['title'])]) 
  bookshelve_body=bookshelve_body+'</td></tr></table>'
  return bookshelve_body
  
@app.route('/<idNumber>/detail.html')
def bookDetail(idNumber):
  detail_body='<table border cellpadding=5> <tr> <td> <h3>Book Details:</h3>'
  entry=Shelve.title_info(idNumber)
  detail_body='</td></tr><tr><td>'.join([detail_body,'Title: %s' % entry['title'],'Author: %s' % entry['author'],'Publisher: %s' % entry['publisher'],'ISBN: <a href=http://www.isbnsearch.org/isbn/%s>%s</a>' % (entry['isbn'],entry['isbn'])])
  detail_body=detail_body+'</td></tr></table>'
  return detail_body
  
if __name__ == '__main__':
  app.run(host='0.0.0.0')