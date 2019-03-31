#! /usr/bin/env python3
import cgi

import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import credentials as login
from common import FormError

def check_validity():
    form = cgi.FieldStorage()
    #TODO: add check for empty form
    if("playerName" not in form):
        raise FormError("Form contains insufficient data.")
        return
    else:
        pname = form["playerName"].value
    
    if pname.isalpha() and len(pname) < 100:
        conn  = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
        c=conn.cursor()
        query = """INSERT INTO gamedata (playerName,choicepath,items,winstatus,dead) VALUES (%s,%s,%s,%s,%s)"""
        c.execute(query, (pname, "", "", 0, 0))
        conn.commit()
        gameID = c.lastrowid
        c.close()
        conn.close()
        return gameID;
    else:
        raise FormError("Player names can only alphanumeric characters and must be of length <100.")
        return

try:
    gameID = check_validity()
    IP = login.webhost['host']

    # https://en.wikipedia.org/wiki/Post/Redirect/Get
    # https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python
    print("Status: 303 See other")
    #remember to update this to the unfinalized url
    print("""Location: http://%s/cgi-bin/mainMenu.py?new_game=%s"""%(IP,gameID))
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
