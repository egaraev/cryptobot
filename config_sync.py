import MySQLdb
import sys



def main():
    print('Starting api keys sync module')

    PS()


def PS():
    api_key=api_key_get()
    api_secret=api_secret_get()
    consumer_key=consumer_key_get()
    consumer_secret=consumer_secret_get()
    access_token=access_token_get()
    access_token_secret=access_token_secret_get()

    print api_key, api_secret

    with open('config.py', 'w') as f:
        f.write("key = "+api_key)
        f.write("\n")
        f.close()

    with open('config.py', 'a') as f:
        f.write("secret = "+api_secret)
        f.write("\n")
        f.close()


    with open('config.py', 'a') as f:
        f.write("consumer_key = "+consumer_key)
        f.write("\n")
        f.close()


    with open('config.py', 'a') as f:
        f.write("consumer_secret = "+consumer_secret)
        f.write("\n")
        f.close()


    with open('config.py', 'a') as f:
        f.write("access_token = "+access_token)
        f.write("\n")
        f.close()


    with open('config.py', 'a') as f:
        f.write("access_token_secret = "+access_token_secret)
        f.close()






def api_key_get():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT api_key FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



def api_secret_get():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT api_secret FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



def consumer_key_get():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT consumer_key FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0




def consumer_secret_get():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT consumer_secret FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



def access_token_get():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT access_token FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0


def access_token_secret_get():
    db = MySQLdb.connect("database-service", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT access_token_secret FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0




if __name__ == "__main__":
    main()