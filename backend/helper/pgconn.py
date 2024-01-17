import sys
import psycopg2
import time

con = cur = db = None

def connect():
    global con, cur, db
    while True:
        try:
            con = psycopg2.connect(
                database='postgres',
                user='postrges',
                password='postgres',
                host='db-thesis',
                port='5432'
                )
            cur = con.cursor()
            print("Connection Open")
            break
        except (psycopg2.DatabaseError):
            if con:
                con.rollback()
            print(psycopg2.DatabaseError)
            print("Retry db connections in 5 seconds")
            time.sleep(5)
            print("Retry connection")
            # sys.exit()


def get_db():
    if not (con and cur and db):
        connect()
    return (con, cur, db)
