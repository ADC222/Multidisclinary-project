import sys
from Adafruit_IO import MQTTClient


AIO_USERNAME = "Vijt"
AIO_KEY = "aio_BtDs44UjEGnzt7mS22RHrtiSzb8P"

def connected(client):
    print("Ket noi thanh cong ...")
    client.subscribe("button1")
    client.subscribe("ai")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    pass