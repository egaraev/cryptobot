import MySQLdb
import sys



def main():
    print('Starting api keys sync module')

    PS()


def PS():
    api_key=api_key_get()
    api_secret=api_secret_get()

    print api_key, api_secret

    with open('config.py', 'w') as f:
        f.write("key = "+api_key)
        f.write("\n")
        f.close()

    with open('config.py', 'a') as f:
        f.write("secret = "+api_secret)
        f.close()




def api_key_get():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT api_key FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0



def api_secret_get():
    db = MySQLdb.connect("localhost", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    cursor.execute("SELECT api_secret FROM parameters")
    r = cursor.fetchall()
    for row in r:
        return (row[0])
    return 0




if __name__ == "__main__":
    main()