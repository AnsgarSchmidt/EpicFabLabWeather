import time
import paho.mqtt.client as mqtt
from Wunderground   import Wunderground
from OpenWeatherMap import OpenWeatherMap

mymqtt    = mqtt.Client("gateways", clean_session=True)
mydata    = {}
connected = False

def _on_connect(client, userdata, rc, msg):
    print ("Connected %s with result code %s" % (client, rc))
    global connected
    connected = True
    mymqtt.subscribe("#")


def _on_disconnect(client, userdata, msg):
    print ("Disconnect %s" % client)
    global connected
    connected = False

def _on_message(client, userdata, msg):
    #print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))
    mydata[msg.topic] = msg.payload

wunderground = Wunderground(mydata)
wunderground.start()

openweathermap = OpenWeatherMap(mydata)
openweathermap.start()

mymqtt.on_connect    = _on_connect
mymqtt.on_message    = _on_message
mymqtt.on_disconnect = _on_disconnect

while True:
    try:

        if not connected:
            mymqtt.connect("172.26.2.9", 1883)
            mymqtt.loop_start()

    except Exception as e:
        print e

    time.sleep(10)
