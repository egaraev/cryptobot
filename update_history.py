import MySQLdb
#orderid=4

for orderid in range(0, 90):
   
	try:
    		db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    		cursor = db.cursor()
    		cursor.execute('SELECT GROUP_CONCAT(signals) FROM orderlogs where orderid=("%s")' % orderid)
    		history = cursor.fetchone()
    		cursor.execute('update orders set history=%s where order_id=%s',(history, orderid))
    		db.commit()
	except MySQLdb.Error, e:
    		print "Error %d: %s" % (e.args[0], e.args[1])
    		sys.exit(1)
	finally:
    		db.close()
