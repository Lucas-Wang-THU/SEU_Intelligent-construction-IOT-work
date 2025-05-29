import random
import time
from paho.mqtt import client as mqtt_client

# 连接信息
broker = 'stevenhou.xyz'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 100)}'
user_name = 'student'
password = 'STUDENT'

# 订阅的主题
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
    # 有消息来的回调
    def on_message(client, userdata, msg):
        # 通过msg.payload.decode()获取消息内容，通过msg.topic获取主题
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    # 执行订阅操作，并指定消息回调
    client.subscribe(topic)
    client.on_message = on_message

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


# 主函数，创建连接，订阅主题
def run():
    client = connect_mqtt()
    sign = int(input("请问是要发布(1)还是接受(2):"))
    while True:
        if sign == 1:
            publish(client)
            client.loop_forever()
        elif sign == 2:
            subscribe(client)
            client.loop_forever()
        else:
            print("请重新输入")

if __name__ == '__main__':
    run()