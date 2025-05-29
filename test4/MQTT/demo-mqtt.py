# from paho.mqtt import client as mqtt_client
#import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import pymysql
import json


# 数据库连接信息，请根据实际情况修改
connection = pymysql.connect(host='cn.stevenhou.xyz',
                                port=3306,
                                user='student00',
                                password='STUDENT00',
                                database='student00')


# MQTT连接信息，请根据实际情况修改，client_id避免重名
broker = 'cn.stevenhou.xyz'
port = 1883
client_id = 'python-mqtt-student00'
user_name = 'student'
password = 'STUDENT'


# 订阅的主题，请根据实际情况修改，避免与他人共用主题
topic = "/student18/stress"


# 连接Broker
def connect_mqtt():
    # 连接后的回调函数，打印是否成功信息
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # 创建一个client，通过client_id来初始化命名
    client = mqtt_client.Client(client_id)
    # 设定用户名密码
    client.username_pw_set(user_name, password)
    # 指定连接后回调函数
    client.on_connect = on_connect
    # 执行连接操作
    client.connect(broker, port)
    return client


# 订阅主题
def subscribe(client):
    # 有消息来的回调，根据需要动态修改
    # 这里假定消息格式如下，解析后存入数据库
    # {
    #   "time": "2023-05-01 00:00:00",
    #   "value": 114514
    # }
    def on_message(client, userdata, msg):
        # 通过msg.payload.decode()获取消息内容，通过msg.topic获取主题
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = json.loads(msg.payload.decode())
        time = data["time"]
        value = data["value"]
        sql = f'''  INSERT INTO stress_data 
                    (time, value)
                    VALUES
                    ( '{time}', {value} )  '''
        cursor = connection.cursor()
        connection.ping()
        cursor.execute(sql)
        connection.commit()


    # 执行订阅操作，并指定消息回调
    client.subscribe(topic)
    client.on_message = on_message


# 主函数，创建连接，订阅主题
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()


