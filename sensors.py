import time
import board
import adafruit_dht
from Adafruit_IO import Client, Feed, RequestError
import RPi.GPIO as GPIO

ADAFRUIT_IO_USERNAME = "your_AIO_USERNAME"
ADAFRUIT_IO_KEY = "your_AIO_KEY"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try:
    temperature_feed = aio.feeds('temperature')
except RequestError:
    temperature_feed = aio.create_feed(Feed(name='temperature'))

try:
    humidity_feed = aio.feeds('humidity')
except RequestError:
    humidity_feed = aio.create_feed(Feed(name='humidity'))

try:
    moisture_feed = aio.feeds('moisture')
except RequestError:
    moisture_feed = aio.create_feed(Feed(name='moisture'))

dht_device = adafruit_dht.DHT22(board.D4)

channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Water Detected!")
        aio.send_data(moisture_feed.key, 100)
    else:
        print("Water Not Detected!")
        aio.send_data(moisture_feed.key, 0)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temperature: {temperature} C")
        print(f"Humidity: {humidity} %")
        aio.send_data(temperature_feed.key, temperature)
        aio.send_data(humidity_feed.key, humidity)
    except RuntimeError as error:
        print(error.args[0])
    time.sleep(5)
