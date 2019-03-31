#! /usr/bin/env python3
import cgi

import cgitb
cgitb.enable()

import MySQLdb
import credentials as login
from common import FormError

def check_validity():
    form = cgi.FieldStorage()
    #TODO: add check for empty form
    if(len(form)==0):
        #raise FormError("Player names can only alphanumeric characters and must be of length <100.")
        #return
        playerName = 'abc'
    else:
        playerName = form["playerName"].value
    if playerName.isalpha() and len(playerName) < 100:
        conn = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
        c=conn.cursor()
        c.execute("""INSERT INTO gamedata (playerName,choicepath,items,winstatus,dead)
              VALUES (%s,'','',0,0)"""%(playerName))
        conn.commit()
        c.close()
        conn.close()
        
        return cursor.lastrowid;
    else:
        raise FormError("Player names can only alphanumeric characters and must be of length <100.")
        return

try:
    print("Content-Type: text/plain")
    gameID = check_validity()
    IP = login.webhost['host']

    # https://en.wikipedia.org/wiki/Post/Redirect/Get
    # https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python
    print("Status: 303 See other")
    #remember to update this to the unfinalized url
    print("""Location: http://%s/cgi-bin/mainMenu.py?new_game=%s"""%(IP,gameID))
    print()
    
except FormError as e:
    print("""Content-Type: text/plain;charset=utf-8
<html>
<head><title>Seventh Cirle - Kyler Novotny</title></head>
<body>
<p>ERROR: %s
<p><a href="mainMenu.py">Return to main menu.</a>
</body>
</html>
""" % e.msg, end="")

except:
    raise    # throw the error again, now that we've printed the lead text - and this will cause cgitb to report the error

