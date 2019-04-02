#! /usr/bin/env python3
import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable()

import MySQLdb
from common import FormError
import credentials as login

def write_html():
    form = cgi.FieldStorage()

    if"new_game" in form:
        new_game = int(form["new_game"].value)
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

    conn = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
    c=conn.cursor()
    c.execute("SELECT * FROM gamedata WHERE winstatus=False AND dead=False")

    activegames = []
    for row in c.fetchall():
        activegames.append({'id':row[0],
                            'playerName':row[1],
                            'choicepath':row[2],
                            'items':row[3],
                            'winstatus':row[4],
                            'dead':row[5]})
    
    wongames = []
    c.execute("SELECT * FROM gamedata WHERE winstatus=True OR dead=True")
    for row in c.fetchall():
        wongames.append({'id':row[0],
                         'playerName':row[1],
                         'choicepath':row[2],
                         'items':row[3],
                         'winstatus':row[4],
                         'dead':row[5]})
    c.close()
    conn.close()
    
    #hardcoded game
    g=[{"gameId":1,"PlayerName":"Thomas","Items":['bow','knife'],"state":"Died"}]
    
    write_table("Active Games",activegames,new_game=new_game,finished=False)
    write_create_game_form()
    write_table("Completed Games",wongames,new_game=new_game,finished=True)

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

    
def write_table(tablename, games, new_game=None, finished=False):
    if finished:
        finishedStr = "<th>Won</th><th>Died</th>"
    else:
        finishedStr = "<th>Continue?</th>"
    if new_game != None:
        color = 'red'
    print("""
<p><b>%s</b>
<table>
<tbody>
<tr>
<th>GameID</th>
<th>Player Name</th>
<th>Items</th>
%s
</tr>
""" % (tablename,finishedStr) ,end="")

    for g in games:
        gameId = g["id"]
        playerName = g["playerName"]
        items = g["items"]
        
        winstatus = g['winstatus']
        dead = g['dead']
        
        if not finished:
            if(new_game is not None and int(gameId)==int(new_game)):
                play="""<td><b><a href="htmlGen.py?gameId=%s">Yes</a></b></td>    """ % gameId
            else:
                play = """<td><a href="htmlGen.py?gameId=%s">Yes</a></td>    """ % gameId
        else:
            play = """ <td>%s</td>""" % winstatus + """<td>%s</td>"""%dead
        print("""
<tr>
<td>%s</td>
<td>%s</td>
<td>%s</td>
%s
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
