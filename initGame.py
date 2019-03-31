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
        raise FormError("Form contains insufficient data.")
        return
    else:
        pname = form["playerName"].value
    conn  = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
    c=conn.cursor()
    
    if pname.isalpha() and len(pname) < 100:
        
        query = """INSERT INTO gamedata (playerName,choicepath,items,winstatus,dead) VALUES (%s,%s,%s,%s,%s)"""
        c.execute(query, (pname, "", "", 0, 0))
        conn.commit()
        gameID = c.lastrowid
        c.close()
        conn.close()
        return gameID;
    else:
        raise FormError("Player names can only alphanumeric characters and must be of length <100.")
        c.close()
        conn.close()
        return

try:
    gameID = check_validity()
    print("Content-Type: text/html")
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
<p>ERROR: %s
<p><a href="mainMenu.py">Return to main menu.</a>
</body>
</html>
""" % e.msg, end="")

except:
    raise    
