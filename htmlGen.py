#! /usr/bin/env python3

import cgi
import cgitb
cgitb.enable()

import MySQLdb
import credentials as login

from common import FormError, get_avail_choices

def write_dead_screen(situation):
    print("""
<body>
<h1> Seventh Circle </h1>
<p>%s</p>
<p>
YOU HAVE DIED
<p><a href="mainMenu.py">Return to main menu.</a></p>
</body>
</p>"""%situation)

def write_win_screen():
    print("""
<body>
<h1> Seventh Circle </h1>
<p>
YOU HAVE WON
<p><a href="mainMenu.py">Return to main menu.</a></p>
</body>
</p>""")

    
    print("""</html""")
def write_html():
    
    #first check for valid gameId
    form = cgi.FieldStorage()
    if "gameId" not in form:
        raise FormError("ID is not in form")
    else:
        gameId = int(form["gameId"].value)

    conn = MySQLdb.connect(host=login.mysql['host'],
                           user=login.mysql['user'],
                           passwd=login.mysql['passwd'],
                           db=login.mysql['db'])
    c=conn.cursor()
    query = """SELECT * FROM gamedata WHERE id=%s""" % gameId
    c.execute(query)
    if(c.rowcount != 1):
        raise FormError("Invalid game ID")

    gameInfo = c.fetchall()[0]
    pname = gameInfo[1]
    choicepath = gameInfo[2]
    
    items = gameInfo[3].split(",")
    #the structure of my gameInfo table is:
    #id (int),playerName(varchar),choicepath(varchar),items(varchar),winstatus(tinyint),dead(tinyint)
    #if user is holding no items, make a blank list to hold them
    if(gameInfo[3] == ""):
        items = []

    #here i reference common.py, which contains all of my choicepaths (which i plan
    #to add much more of). The structure of my choices dictionary is located there.
    try:
        choices = get_avail_choices(choicepath)
    except KeyError as e:
        print("""

<html>
<head><title>Seventh Cirle - Kyler Novotny</title></head>
<body>
<p>ERROR: Path not added to choices yet.</p>
<p><a href="mainMenu.py">Return to main menu.</a></p>
</body>
</html>
""", end="")
        return
        
                             
    currentSituation = choices[1]
    if(gameInfo[4]==True):
        write_win_screen()
        return
    if(gameInfo[5]==True):
        write_dead_screen(currentSituation)
        return 

    #choice text
    choiceStr="""
<form action="update.py" method="post">
<input type="hidden" name="gameId" value=%s>
<table>
<tbody>
"""%gameId
    
    possible = choices[3:]
    i = 0
    #go through all possible choices from current point
    for num in possible:
        i+=1
        if(i-1)%2==0:
            choiceStr+="<tr>"
        #get next choice's info
        try:
            nextChoice = get_avail_choices(choicepath+str(num));
        except KeyError as e:
            print("""

<html>
<head><title>Seventh Cirle - Kyler Novotny</title></head>
<body>
<p>ERROR: Path not added to choices yet.</p>
<p><a href="mainMenu.py">Return to main menu.</a></p>
</body>
</html>
""", end="")
            return

        desc = nextChoice[0]
        if(len(nextChoice)>=3):
            req = nextChoice[2]
        if(len(nextChoice)==2):
            choiceStr += """<td>%s<button type="submit" name="dead" value="%s"></button></td>"""% (nextChoice[0],i)
        elif(len(nextChoice)==3 and nextChoice[1] == "YOU WON"):
            choiceStr += """<td>%s<button type="submit" name="win" value="%s"></button></td>"""% (nextChoice[0],i)
        #make sure that the required items for that choice are held
        #and item is not already in inventory
        elif(req == None) or (req in items):
            #if the next choice is an item pickup
            if len(nextChoice)==3 and (nextChoice[1] not in items):
                choiceStr += """<td>%s<button type="submit" name="item" value="%s"></button></td>"""% (nextChoice[0],nextChoice[1])
            #if the next choice is a choice
            elif nextChoice[1] not in items:
                choiceStr+="""<td>%s<button type="submit" name="choice" value="%s"></button></td>"""%(nextChoice[0],i)

        if(i)%2==0:
            choiceStr+="</tr>"

    choiceStr+="""
</tbody>
</table>
</form>"""

#then start printing the game headings
    print("""<!DOCTYPE html>
<html>
<head><title>Seventh Circle - Kyler Novotny</title>
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
</head>
""")
    
    #current situation text
    print("""
<body>
<h1> Seventh Circle </h1>
<p>
%s
</p>
<div>
<p> Would you like to:</p>
"""%currentSituation)
    
    #print choices table
    print(choiceStr)
                    
# HERE FOR THE FORM ACTION, NEED UPDATE PY SCRIPT
# below is the general html formatting of the printed choiceStr.
##
##    choiceStr="""
##<form action="update.py" method="post">
##<table>
##<tbody>
##<tr>
##<td>CHOICE1<button type=“submit” name=item/choice value=“1”></button></td>
##<td>CHOICE2<button type=“submit” name=item/choice value=“2”></button></td>
##</tr>
##<tr>
##<td>CHOICE3<button type=“submit” name=choice value=“3”></button></td>
##<td>CHOICE4<button type=“submit” name=choice value=“4”></button></td>
##</tr>
##</tbody>
##</table>
##</form>
##"""

    #now to generate the table of items (inventory)
    itemStr = """
</div>
<br>
<table>
<tr><th colspan=2>Inventory</th></tr>
"""
    for index in range(len(items)):
        if(index%2==0):
            itemStr += """<tr>"""
            
        itemStr += """<td>%s</td>""" % items[index]

        if(index%2==1):
            itemStr += """</tr>"""
    for index in range(len(items),8):
        if(index%2==0):
            itemStr += """<tr>"""
            
        itemStr += """<td>-</td>"""

        if(index%2==1):
            itemStr += """</tr>"""

    itemStr+="""
</table>
</body>
</html>"""

    print(itemStr)

# here is the general layout of my inventory table
##    itemStr+="""
##<tr><td>ITEM1</td><td>ITEM2</td></tr>
##<tr><td>ITEM3</td><td>ITEM4</td></tr>
##<tr><td>ITEM5</td><td>ITEM6</td></tr>
##<tr><td>ITEM7</td><td>ITEM8</td></tr>
##</table>
##</body>
##</html>"""



try:
    print("Content-Type: text/html")
    print()
    write_html()
except FormError as e:
    print("""

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
