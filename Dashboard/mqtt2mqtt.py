import time
import ConfigParser
import paho.mqtt.client as mqtt

config = ConfigParser.ConfigParser()
config.read("config.ini")
intern = mqtt.Client("Mqtt2Mqtt", clean_session=True)
extern = mqtt.Client("Mqtt2Mqtt", clean_session=True)

def _on_connect(client, userdata, rc, msg):
    #print ("Connected %s with result code %s" % (client, rc))
    intern.subscribe("#")


def _on_disconnect(client, userdata, msg):
    pass
    #print ("Disconnect %s" % client)


def _on_message(client, userdata, msg):
    #print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))
    extern.publish(msg.topic, msg.payload)

intern.on_connect    = _on_connect
intern.on_message    = _on_message
intern.on_disconnect = _on_disconnect
intern.connect(config.get("intern", "host"), int(config.get("intern", "port")))
intern.loop_start()

extern.username_pw_set(config.get("extern", "user"), config.get("extern", "passwd"))
extern.on_connect    = _on_connect
extern.on_disconnect = _on_disconnect
extern.connect(config.get("extern", "host"), int(config.get("extern", "port")))
extern.loop_start()

while True:
    time.sleep(100)
