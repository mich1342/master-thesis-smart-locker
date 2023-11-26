from fastapi import APIRouter, Response
import helper.pgconn as pgconn

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

conn, cur, db = pgconn.get_db()

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not Found"}},
)

@router.post('/init_db', status_code=200)
async def init_db(response:Response):
    cur.execute('''
                DROP TABLE IF EXISTS transaction;
                CREATE TABLE transaction (
                    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    locker VARCHAR(20),
                    box VARCHAR(20),
                    package_code VARCHAR(40),
                    qr_code VARCHAR(40),
                    status VARCHAR(20)
                );
                INSERT INTO transaction (locker, box, qr_code, status)
                VALUES
                ('AAA', '001', 'idle', 'IDLE'),
                ('AAA', '002', 'idle', 'IDLE'),
                ('AAA', '003', 'idle', 'IDLE');
                ''')
    conn.commit()
    return {"msg": "Successfully Initialized DB"}

