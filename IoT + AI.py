print("MQTT with Adafruit IO")
import time
import random
import sys
import requests
from Adafruit_IO import MQTTClient


from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import cv2

#AI set up
camera= cv2.VideoCapture(0)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("A:/MP/New folder/keras_Model.h5", compile=False)


# Load the labels
class_names = open("A:/MP/New folder/labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def image_detector():
    ret, image= camera.read()
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    cv2.imshow("Webcam Image", image)
    image= np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image/127.5) -1
    prediction=model.predict(image)
    index=np.argmax(prediction)
    class_name=class_names[index]
    confidence_score= prediction[0][index]
    print("class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2],"%")


size = (224, 224)


# Predicts the model
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]



# IoT set up
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
    image_detector()
    time.sleep(5)
    s1 = random.randint(0,100)
    s2 = random.randint(0,100)
    s3 = random.randint(0,100)
    client.publish("temperature", s1)
    client.publish("humidity", s2)
    client.publish("moisture", s3)
    client.publish("prediction", class_name[2:])
    pass

