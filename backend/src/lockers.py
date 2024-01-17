from fastapi import APIRouter, Response
import helper.pgconn as pgconn

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from pydantic import BaseModel
from fastapi_mqtt import FastMQTT, MQTTConfig

import string
import random

conn, cur, db = pgconn.get_db()

router = APIRouter(
    prefix="/api/lockers",
    tags=["Lockers"],
    responses={404: {"description": "Not Found"}},
)

mqtt_config = MQTTConfig(
    host="mqtt-broker",
    port=1883,
    keepalive=60
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(router)
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("+/+/transaction_done") 
    print("Connected: ", client, flags, rc, properties)
    cur.execute(f'''
                    SELECT 
                        locker,
                        box
                    FROM
                        transaction
                ''')
    res = cur.fetchall()
    for x in res:
        print(x)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    msg = payload.decode()
    try:
        val = topic.split("/")
        print(val)
        if val[2] == "transaction_done":
            if(msg == "1"):
                cur.execute(f'''
                                UPDATE 
                                    transaction
                                SET
                                    status = 'IDLE',
                                    qr_code = 'idle',
                                    package_code = Null
                                WHERE
                                    locker = '{val[0]}'
                                    AND
                                    box = '{val[1]}'
                            ''')
                conn.commit()
                mqtt.publish(f"{val[0]}/{val[1]}/qr", f"idle", 1, True)
                
    except Exception as ex:
        print(ex)           
        

@router.get('/', status_code=200)
async def get_lockers_info(response:Response):
    cur.execute('''
                SELECT row_to_json(row) FROM 
                (
                    SELECT
                        t.id,
                        t.locker,
                        t.box,
                        t.status,
                        t.package_code,
                        t.qr_code
                    FROM
                        transaction as t
                )
                row;
                ''')
    res = cur.fetchall()
    temp_res = []
    for x in res:
        temp_res.append(x[0])
    return {"msg": temp_res}

class AssignLocker(BaseModel):
    locker: str
    box: str
    package_code: str
    
@router.post('/assign', status_code=200)
async def assign_locker(assign_locker: AssignLocker, response:Response):
    cur.execute(f'''
                SELECT 
                    status
                FROM 
                    transaction
                WHERE
                    locker = '{assign_locker.locker}'
                    AND
                    box = '{assign_locker.box}'
                ''')
    res = cur.fetchall()
    if res[0][0] != "IDLE":
        response.status_code = 400
        return {"msg": "Slot is not available, try another slot"}
    qr_code = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=8))
    cur.execute(f'''
                UPDATE 
                    transaction
                SET
                    status = 'INBOUND',
                    qr_code = '{qr_code}',
                    package_code = '{assign_locker.package_code}'
                WHERE 
                    locker = '{assign_locker.locker}'
                    AND
                    box = '{assign_locker.box}'
                ''')
    conn.commit()
    mqtt.publish(f"{assign_locker.locker}/{assign_locker.box}/qr", f"{qr_code}", 1, True)
    return {"msg": f"Successfully Inbound Package {assign_locker.package_code}"}

class PickupPackage(BaseModel):
    package_code: str
    
@router.post('/pickup', status_code=200)
async def pickup_package(pickup_package: PickupPackage, response:Response):
    try:
        cur.execute(f'''
                    SELECT 
                        locker,
                        box,
                        status
                    FROM 
                        transaction
                    WHERE
                        package_code = '{pickup_package.package_code}'
                    ''')
        res = cur.fetchall()
    except Exception as e:
        print(e)
        response.status_code = 400
        return {"msg": "Package is not Ready / Invalid Package Code"}
    if len(res) == 0:
        response.status_code = 400
        return {"msg": "Package is not Ready / Invalid Package Code"}
    
    res = res[0]
    
    if(res[2] != "INBOUND"):
        response.status_code = 400
        return {"msg": "Package is already claimed"}
    return {
            "msg": f"Please claim your package at Locker {res[0]} Box {res[1]}",
            "data": {
                "locker": res[0],
                "box": res[1]
            }
        }
    
@router.post('/ping', status_code=200)
async def ping_locker(pickup_package: PickupPackage, response:Response):
    try:
        cur.execute(f'''
                    SELECT 
                        locker,
                        box,
                        status
                    FROM 
                        transaction
                    WHERE
                        package_code = '{pickup_package.package_code}'
                    ''')
        res = cur.fetchall()
    except Exception as e:
        print(e)
        response.status_code = 400
        return {"msg": "Package is not Ready / Invalid Package Code"}
    if len(res) == 0:
        response.status_code = 400
        return {"msg": "Package is not Ready / Invalid Package Code"}
    
    res = res[0]
    
    if(res[2] != "INBOUND" and res[2] != "DOOR_OPEN"):
        response.status_code = 400
        return {"msg": "Package is already claimed"}
    mqtt.publish(f"{res[0]}/{res[1]}/lamp_ping", "PING")
    return {
            "msg": f"Successfully Ping Locker {res[0]} Box {res[1]}",
        }
    
    
class OpenDoor(BaseModel):
    package_code: str
    qr_code: str

@router.post('/open_door', status_code=200)
async def open_door(open_door: OpenDoor, response:Response):
    print(open_door)
    try:
        cur.execute(f'''
                    SELECT 
                        locker,
                        box,
                        status
                    FROM 
                        transaction
                    WHERE
                        package_code = '{open_door.package_code}'
                        AND
                        qr_code = '{open_door.qr_code}'
                    ''')
        res = cur.fetchall()
    except Exception as e:
        print(e)
        response.status_code = 400
        return {"msg": "Package is not Ready / Invalid Package Code"}
    if len(res) == 0:
        response.status_code = 400
        return {"msg": "Package is not Ready / Invalid Package Code"}
    
    res = res[0]
    
    if(res[2] != "INBOUND" and res[2] != "DOOR_OPEN"):
        response.status_code = 400
        return {"msg": "Package is already claimed"}
    
    mqtt.publish(f"{res[0]}/{res[1]}/door_command", "OPEN")
    cur.execute(f'''
                UPDATE 
                    transaction
                SET
                    status = 'DOOR_OPEN'
                WHERE
                    package_code = '{open_door.package_code}'
                    AND
                    qr_code = '{open_door.qr_code}'
                ''')
    conn.commit()
    return {
            "msg": f"Door Open",
        }

