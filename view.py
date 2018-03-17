#!/usr/bin/python
import cgi
import cgitb
import MySQLdb
import requests
import time
cgitb.enable()




# Connect to MySQL database
db = MySQLdb.connection(host="127.0.0.1",
                user="cryptouser",
                passwd="123456",
                db="cryptodb")




#######




# Generate the HTML response

#######################################################

print """content-type: text/html

<html><head><title>Cryptobot</title></head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
</head>
<body bgcolor=#abcaf2><h2>Cryptobot View Page</h2>
<b>Logs</b><br>
<b>Date\Time</b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<b>Action</b><br>
"""

# Read logs
db.query("SELECT * FROM logs order by log_id desc")
r = db.store_result()

history = ""
for row in r.fetch_row(10):
    history += "<font size='2'>"+ cgi.escape(row[1])  + cgi.escape(row[2]) + "</font>" + "<br>\n"


print history



# Read orders
db.query("SELECT * FROM orders where active = 1")
r = db.store_result()

orders = ""
for row in r.fetch_row(10000):
    orders += "<font size='2'>" + cgi.escape(row[5]) + "&nbsp&nbsp&nbsp" + cgi.escape(row[7]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"  + cgi.escape(row[1])   + "&nbsp&nbsp&nbsp" + cgi.escape(row[2]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[3]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[8])  + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[12]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"  + cgi.escape(row[9]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[11]) + "</font>" + "<br>\n"


print """
<b>Current orders</b><br>
<b>Date</b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<b><b>Iteration&nbsp&nbsp&nbsp&nbsp </b>Market&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Quantity&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Price&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Current result in BTC&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Current result in USD&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Reason and Parameters used&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>&nbsp&nbspPrevious deficit BTC</b><br>
"""
print orders





# Read completed orders
db.query("SELECT * FROM orders where active = 0")
r = db.store_result()

comporders = ""
for row in r.fetch_row(10000):
    comporders += "<font size='2'>" + cgi.escape(row[5]) + "&nbsp&nbsp&nbsp"  + cgi.escape(row[7]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"  + cgi.escape(row[1])  + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[2]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[3]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[8]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"  + cgi.escape(row[12]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" +  cgi.escape(row[9]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + cgi.escape(row[10]) + "</font>" + "<br>\n"


print """
<b>Completed orders</b><br>
<b>Date</b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<b>Iteration&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Market&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Quantity&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Price&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Current result in BTC&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Current result in USD&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b>Reason and Parameters used &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><b> Reason to sell &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b><br>
"""
print comporders






# Read BTC Price
db.query("SELECT * FROM parameters")
r = db.store_result()
BTC_price = ""

for row in r.fetch_row(1):
    BTC_price += "USDT-BTC" + "&nbsp&nbsp&nbsp&nbsp"  + cgi.escape(row[10]) + "<br>\n"


print """
<b>Price for Bitcoin</b><br>
"""
print BTC_price



#Count the summ of closed orders
db.query("SELECT SUM(serf_usd) FROM orders where active = 0")
r = db.store_result()
SUMM = ""

for row in r.fetch_row(1):
 SUMM += "Total summ" +  "&nbsp&nbsp&nbsp&nbsp"  + cgi.escape(row[0]) + "<br>\n"

print """
<b>Total summ</b><br>
"""
print SUMM


