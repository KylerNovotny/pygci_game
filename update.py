#! /usr/bin/env python3

import cgi

import cgitb
cgitb.enable()

import MySQLdb
import credentials as login
from common import FormError

def check_validity():
    form = cgi.FieldStorage()
    
    print(1)
    if("item" not in form and "choice" not in form) or ("gameId" not in form):
        raise FormError("Form does not contain a decision.")
        return
    
    gameId = form["gameId"].value
    
    if("item" in form):
        item = form["item"].value
    else:
        choice = form["choice"].value
        
    conn  = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
    c=conn.cursor()
    query = """SELECT * FROM gamedata WHERE id=%s""" % gameId
    c.execute(query)
    if(c.rowcount != 1):
        raise FormError("Invalid game ID")
    gameInfo = c.fetchAll()[0]
    choicepath = gameInfo[2]
    items = gameInfo[3].split(",")

    
    if("item" in form):
        items.append(item)
        query = """UPDATE gamedata SET items=%s WHERE id=%s"""%(items,gameId)
    else:
        query = """UPDATE gamedata SET choicepath=%s WHERE id=%s"""%(choicepath+choice,gameId)

    c.execute(query)
        
    conn.commit()
    c.close()
    conn.close()
    return gameId

try:
    gameId = check_validity()
    IP = login.webhost['host']
    
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
