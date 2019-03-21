#! /usr/bin/env python3
import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable()

import MySQLdb
from common import FormError

def write_html():
    form = cgi.FieldStorage()

    if"new_game_id" in form:
        new_game = int(form["new_game_id"].value)
    else:
        new_game = None
    
    print("""<html>
<head><title>Seventh Circle - Kyler Novotny</title></head>
<style>
th, td {
text-align: center;
border: 1px solid black;
}
table{
width: 50%;
float: none;
border: 1px solid black;
}
button{
height: “50”
width: “50”
}
</style>
<body>
""",end="")

    #HTML GENERATION HERE
    
    #hardcoded game
    g=[{"gameId":1,"PlayerName":"Thomas","Items":['bow','knife'],"state":"Died"}]
    
    write_table("Active Games",g,finished=False)
    write_create_game_form()
    write_table("Completed Games",g,finished=True)

    print("""</body>
</html>
""",end="")

    
def write_create_game_form():
    print("""
<form action="initGame.py" method="post">
Player Name<input type="text" name="playerName">
<input type=submit value="New Game">
</form>
""", end="")

    
def write_table(name, games, new_game=None, finished=False):
    #TODO: implement HTML generating code for tables here
    if finished:
        finishedStr = "<th>Won/Died</th>"
    else:
        finishedStr = "<th>Continue?</th>"

    print("""
<p><b>%s</b>
<table>
<tbody>
<tr>
<th>gameID</th>
<th>playerName</th>
<th>items</th>
%s
</tr>
""" % (name,finishedStr) ,end="")

    for g in games:
        gameId = g["gameId"];
        playerName = g["PlayerName"]
        items = g["Items"]
        
        if not finished:
            play = """<a href="htmlGen.py?gameId=%s">Yes</a>    """ % gameId
        else:
            play = g["state"]
        print("""
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
</tr>
""" % (gameId,playerName,items,play),end="")



    print("""
</table>
</p>
""",end="")
    

#This is what runs when the page is first loaded each time.

print("Content-Type: text/html;charset=utf-8")
print()

write_html()
