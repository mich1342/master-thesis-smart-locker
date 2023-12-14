import sys
import psycopg2

con = cur = db = None

def connect():
    global con, cur, db
    try:
        con = psycopg2.connect(
            database='postgres',
            user='postrges',
            password='postgres',
            host='postgres',
            port='5432'
            )
        cur = con.cursor()
        print("Connection Open")
    except (psycopg2.DatabaseError):
        if con:
            con.rollback()
        print(psycopg2.DatabaseError)
        sys.exit


def get_db():
    if not (con and cur and db):
        connect()
    return (con, cur, db)