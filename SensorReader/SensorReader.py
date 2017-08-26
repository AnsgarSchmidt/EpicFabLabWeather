import time
import paho.mqtt.client as mqtt


def _on_connect(client, userdata, rc, msg):
    print ("Connected %s with result code %s" % (client, rc))
    mymqtt.subscribe("buzzer")


def _on_disconnect(client, userdata, msg):
    print ("Disconnect %s" % client)


def _on_message(client, userdata, msg):
    print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))
    # do the buzz here


mymqtt = mqtt.Client("sensors", clean_session=True)
mymqtt.on_connect    = _on_connect
mymqtt.on_message    = _on_message
mymqtt.on_disconnect = _on_disconnect
mymqtt.connect("172.26.2.9", 1883)
mymqtt.loop_start()

while True:

    # testsensor1
    testdata = 23.42
    mymqtt.publish("phalanx/testsensor1", testdata)

    # testsensor1
    testdata = 12.124
    mymqtt.publish("phalanx/testsensor2", testdata)

    time.sleep(10)
