import time
import paho.mqtt.client as mqtt

mymqtt = mqtt.Client("gateways", clean_session=True)


def _on_connect(client, userdata, rc, msg):
    print ("Connected %s with result code %s" % (client, rc))
    mymqtt.subscribe("#")


def _on_disconnect(client, userdata, msg):
    print ("Disconnect %s" % client)


def _on_message(client, userdata, msg):
    print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))


mymqtt.on_connect    = _on_connect
mymqtt.on_message    = _on_message
mymqtt.on_disconnect = _on_disconnect
mymqtt.connect("172.26.2.9", 1883)
mymqtt.loop_forever()

