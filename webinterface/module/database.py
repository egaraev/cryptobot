import pymysql

class Database:
    def connect(self):
        return pymysql.connect("localhost","cryptouser","123456","cryptodb" )
    
    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            if id == None:
                cursor.execute("SELECT * FROM users order by id desc")
            else:
                cursor.execute("SELECT * FROM users where id = %s order by username asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self,data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("INSERT INTO users(username,password) VALUES (%s,%s)", (data['username'],data['password'],))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()
            
    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("UPDATE users set username = %s, password = %s where id = %s", (data['username'],data['password'],id,))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()
        
    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("DELETE FROM users where id = %s", (id,))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()

    def update_settings(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE parameters set buy_size = %s, buy_size2 = %s, sell_size =%s, profit =%s, stop_loss =%s, maxiteration =%s, order_multiplier =%s, min_percent_chg =%s, max_percent_chg =%s, last_orders_quantity =%s, stop_bot =%s  where id = %s",
                           (data['buy_size'], data['buy_size2'], data['sell_size'], data['profit'], data['stop_loss'], data['maxiteration'], data['order_multiplier'], data['min_percent_chg'], data['max_percent_chg'], data['last_orders_quantity'], data['stop_bot'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def read_settings(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM parameters")
            else:
                cursor.execute("SELECT * FROM parameters where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()



    def read_orders(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM orders where active = 1")
            else:
                cursor.execute("SELECT * FROM orders where active = 1 and where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def read_corders(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM orders where active = 0")
            else:
                cursor.execute("SELECT * FROM orders where active = 0 and where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()


    def read_logs(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM logs order by log_id desc")
            else:
                cursor.execute("SELECT * FROM logs order by log_id desc where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def update_market(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute(
                "UPDATE markets set market = %s, buy_orders = %s, sell_orders =%s, active =%s  where id = %s",
                (data['market'], data['buy_orders'], data['sell_orders'], data['active'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()


    def read_markets(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM markets")
            else:
                cursor.execute("SELECT * FROM markets where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
          con.close()

    def delete_markets(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM markets where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def insert_market(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO markets(market,buy_orders,sell_orders, active) VALUES (%s,%s,%s,%s)", (data['market'], data['buy_orders'], data['sell_orders'], data['active'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

