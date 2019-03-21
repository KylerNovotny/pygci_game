#! /usr/bin/env python3
import cgi

import cgitb
cgitb.enable()

import MySQLdb
from common import FormError

def check_validity():
    form = cgi.FieldStorage()
    #TODO: add check for empty form
    playerName = form["playerName"].value
    if playerName.isalpha():
        #here should add game ID using database here
        return 1
    else:
        raise FormError("Player names can only contain upper and lowercase characters.")
        return

try:
    print("Content-Type: text/html")
    gameID = check_validity()

    # https://en.wikipedia.org/wiki/Post/Redirect/Get
    # https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python
    print("Status: 303 See other")
    #remember to update this to the unfinalized url
    print("""Location: http://54.212.32.71/cgi-bin/mainMenu.py?new_game=%s"""%(gameID))
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
    raise    # throw the error again, now that we've printed the lead text - and this will cause cgitb to report the error

