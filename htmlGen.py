#! /usr/bin/env python3

import cgi
import cgitb
cgitb.enable()

import MySQLdb
import credentials as login

from common import FormError, get_avail_choices

def write_html():
    

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
    
    gameInfo = c.fetchall()[0]
    pname = gameInfo[1]
    choicepath = gameInfo[2]
    items = gameInfo[3].split(",")
    if(gameInfo[3] == ""):
        items = []
    
    choices = get_avail_choices(choicepath)
                           
    currentSituation = choices[1]

    #body text
    print("""
<body>
<h1> Seventh Circle </h1>
<p>
%s
</p>
<div>
<p> Would you like to:</p>
"""%currentSituation)

    #choice text
    choiceStr="""
<form action="update.py" method="post">
<table>
<tbody>
"""
    
    
    possible = choices[3:]
    i = 0
    #go through all possible choices from current point
    for num in possible:
        i+=1
        if(i-1)%2==0:
            choiceStr+="<tr>"
        #get next choice's info
        nextChoice = get_avail_choices(choicepath+str(num));
        desc = nextChoice[0]
        req = nextChoice[2]
        print("""<p>: %s</p>"""% nextChoice)
        print("""<p>: %s</p>"""%(req in items))
        print("""<p>: %s</p>"""%(nextChoice[1] not in items))
        #make sure that the required items for that choice are held
        #and item is not already in inventory
        if(req == None) or (req in items):
            #if the next choice is an item pickup
            if len(nextChoice)==3 and (nextChoice[1] not in items):
                choiceStr += """<td>%s<button type="submit" name=item value="%s"></button></td>"""% (nextChoice[0],nextChoice[1])
            #if the next choice is a choice
            else:
                choiceStr+="""<td>%s<button type="submit" name=choice value="%s"></button></td>"""%(nextChoice[0],i)

        if(i)%2==0:
            choiceStr+="</tr>"

    choiceStr+="""
</tbody>
</table>
</form>"""

    print(choiceStr)
                    
# HERE FOR THE FORM ACTION, NEED UPDATE PY SCRIPT
##
##    choiceStr="""
##<form action="update.py" method="post">
##<table>
##<tbody>
##<tr>
##<td>CHOICE1<button type=“submit” name=choice value=“1”></button></td>
##<td>CHOICE2<button type=“submit” name=choice value=“2”></button></td>
##</tr>
##<tr>
##<td>CHOICE3<button type=“submit” name=choice value=“3”></button></td>
##<td>CHOICE4<button type=“submit” name=choice value=“4”></button></td>
##</tr>
##</tbody>
##</table>
##</form>
##"""
    
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
    for index in range(8-len(items)):
        if(index%2==0):
            itemStr += """<tr>"""
            
        itemStr += """<td> </td>"""

        if(index%2==1):
            itemStr += """</tr>"""

    itemStr+="""
</table>
</body>
</html>"""

    print(itemStr)
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
