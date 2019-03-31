#! /usr/bin/env python3

import cgi
import cgitb
cgitb.enable()

import MySQLdb
import credentials as login

from common import FormError

def write_html():

    form = cgi.FieldStorage()
    if len(form)==0:
        raise FormError("ID is not in ")
    
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
<body>
<h1> Seventh Circle </h1>
<p style=“”>
CURRENTSITUATION
</p>
<div>
<p> Would you like to:</p>
<form>
<table>
<tbody>
<tr>
<td>CHOICE1<button type=“submit” name=choice value=“1”></button></td>
<td>CHOICE2<button type=“submit” name=choice value=“2”></button></td>
</tr>
<tr>
<td>CHOICE3<button type=“submit” name=choice value=“3”></button></td>
<td>CHOICE4<button type=“submit” name=choice value=“4”></button></td>
</tr>
</tbody>
</table>
</form>
</div>
<br>
<table>
<tr><th colspan=2>Inventory</th></tr>
<tr><td>ITEM1</td><td>ITEM2</td></tr>
<tr><td>ITEM3</td><td>ITEM4</td></tr>
<tr><td>ITEM5</td><td>ITEM6</td></tr>
<tr><td>ITEM7</td><td>ITEM8</td></tr>
</table>
<br>
<p>HTTP vars:
</p>
<pre>
</body>
</html>""")


try:
    print("Content-Type: text/html")
    print()
    write_html()
except FormError as e:
    print("""Content-Type: text/html;charset=utf-8

<html>

<head><title>346 - Russ Lewis - Tic-Tac-Toe</title></head>
<body>
<p>ERROR: %s
<p><a href="mainMenu.py">Return to main menu.</a>
</body>
</html>
""" % e.msg, end="")

except:
    raise
