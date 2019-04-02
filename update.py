#! /usr/bin/env python3
import cgi

import cgitb
cgitb.enable(display=1, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import credentials as login
from common import FormError

def check_validity():
    form = cgi.FieldStorage()
    
    #TODO: add check for empty form
    if("item" not in form and "choice" not in form):
        raise FormError("Form does not contain a decision.")
        return
    conn  = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
    c=conn.cursor()
    query = """SELECT * FROM gamedata WHERE id=%s""" % gameId
    c.execute(query)
    if(c.rowcount != 1):
        raise FormError("Invalid game ID")
    
    if("item" in form):
        query = """UPDATE gamedata SET items=%s WHERE id=%s"""%()
        
    conn.commit()
    gameID = c.lastrowid
    c.close()
    conn.close()

try:
    check_validity()
    IP = login.webhost['host']

    # https://en.wikipedia.org/wiki/Post/Redirect/Get
    # https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python
    print("Status: 303 See other")
    print("""Location: http://%s/cgi-bin/htmlGen.py?gameId=%s"""%(IP,gameID))
    print()
    
except FormError as e:
    print("""Content-Type: text/html;charset=utf-8

<html>
<head><title>Seventh Cirle - Kyler Novotny</title></head>
<body>
<p>ERROR: %s</p>
<p><a href="mainMenu.py">Return to main menu.</a></p>
</body>
</html>
""" % e.msg, end="")

except:
    raise
