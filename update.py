#! /usr/bin/env python3

import cgi

import cgitb
cgitb.enable(display=1, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import credentials as login
from common import FormError

def check_validity():
    form = cgi.FieldStorage()
    
    
    if ("item" not in form and "choice" not in form and "win" not in form and "dead" not in form) or ("gameId" not in form):
        raise FormError("Form does not contain a decision.")
        return
    
    gameId = int(form["gameId"].value)
    
    if("item" in form):
        item = form["item"].value
    elif("choice" in form):
        choice = str(form["choice"].value)
        
    conn  = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
    c=conn.cursor()
    query = """SELECT * FROM gamedata WHERE id=%s""" % gameId
    c.execute(query)
    if(c.rowcount != 1):
        raise FormError("Invalid game ID")
    gameInfo = c.fetchall()[0]
    choicepath = gameInfo[2]
    items = gameInfo[3].split(",")
    
    if('dead' in form):
        query = """UPDATE gamedata SET dead=1,choicepath=%s WHERE id=%s"""
        choice = str(form['dead'].value)
        c.execute(query,(str(choicepath)+str(choice),gameId))
    elif("win" in form):        
        query = """UPDATE gamedata SET winstatus=1 WHERE id=%s"""%gameId
        c.execute(query)
    elif("item" in form):
        if(gameInfo[3]==""):
            items=item
        else:
            items = gameInfo[3].split(",")
            items.append(item)
            items = ",".join(items)
        query = """UPDATE gamedata SET items=%s WHERE id=%s"""
        c.execute(query,(items,gameId))
    else:
        newchoicepath = str(choicepath) + str(choice)
        query = """UPDATE gamedata SET choicepath=%s WHERE id=%s"""
        c.execute(query,( newchoicepath,gameId))
       
    conn.commit()
    
    c.close()
    conn.close()
    return gameId

try:
    #uncomment this for debugging 500 internal server error
##    print("""Content-Type: text/html;charset=utf-8
##
##""")
    gameId = check_validity()
    IP = login.webhost['host']
    
    print("Status: 303 See other")
    print("""Location: http://%s/cgi-bin/htmlGen.py?gameId=%s"""%(IP,gameId))
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
