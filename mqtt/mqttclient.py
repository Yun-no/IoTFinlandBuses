from config import settings
from datetime import datetime
import paho.mqtt.client as mqtt
import psycopg2
import traceback
import json


def on_message(client, userdata, message):
    print(message.topic + " " + str(message.payload))
    try:
        mqtt_data = json.loads(message.payload.decode('utf-8'))
        bus_id = f"{mqtt_data['VP']['oper']}/{mqtt_data['VP']['veh']}"
        print(bus_id, mqtt_data['VP']['lat'], mqtt_data['VP']['long'], mqtt_data['VP']['stop'],
              datetime.fromtimestamp(mqtt_data['VP']['tsi']))
        db_conn = userdata['db_conn']

        cur = db_conn.cursor()

        insert_sql = '''
            INSERT INTO bus_positions (bus_id, latitude, longitude, next_stop, updated)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (bus_id) DO UPDATE SET
            (latitude, longitude, next_stop, updated) = 
            (EXCLUDED.latitude, EXCLUDED.longitude, EXCLUDED.next_stop, EXCLUDED.updated);
        '''
        cur.execute(insert_sql, (bus_id, mqtt_data['VP']['lat'], mqtt_data['VP']['long'], mqtt_data['VP']['stop'],
                                 datetime.fromtimestamp(mqtt_data['VP']['tsi'])))

        cur.close()

    except Exception as e:
        traceback.print_exc()


def init_mqtt():
    connection = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port
    )
    connection.autocommit = True
    mqtt_client = mqtt.Client()
    mqtt_client.user_data_set({'db_conn': connection})
    try:
        mqtt_client.on_message = on_message
        mqtt_client.connect(settings.mqtt_broker_address, settings.mqtt_broker_port)
        mqtt_client.subscribe(settings.mqtt_broker_topic, qos=1)
        mqtt_client.loop_forever()
    except Exception as e:
        traceback.print_exc()
    finally:
        connection.close()


if __name__ == "__main__":
    init_mqtt()