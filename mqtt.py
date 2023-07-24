print("MQTT with Adafruit IO")
import time
import random
import sys
import requests
from Adafruit_IO import MQTTClient
AIO_USERNAME = "Vijt"
AIO_KEY = ""
global_equation = 'x1 + x2 + x3'


def init_global_equation():
    global global_equation
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/NPNLab_BBC/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global_equation = data["last_value"]
    print("Get lastest value:", global_equation)

def modify_value(x1, x2, x3):
    result = eval(global_equation)
    return result

def connected(client):
    print("Server connected ...")
    client.subscribe("led")
    client.subscribe("waterpump")
    client.subscribe("equation")
def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!!!")

def disconnected(client):
    print("Disconnected from the server!!!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload)
    if(feed_id == "equation"):
        global global_equation
        global_equation = payload
        print(global_equation)

client = MQTTClient("Vijt", "")

client.on_connect = connected  #function pointer
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()
init_global_equation()


while True:
    time.sleep(5)
    s1 = random.randint(0,100)
    s2 = random.randint(0,100)
    s3 = random.randint(0,100)
    client.publish("temperature", s1)
    client.publish("humidity", s2)
    client.publish("moisture", s3)
    client.publish("prediction", "healthy")
    #s4 = modify_value(s1, s2, s3)
    #print(s4)
    pass



