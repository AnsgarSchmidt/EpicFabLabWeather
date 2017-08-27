import time
import ConfigParser
import paho.mqtt.client as mqtt

config           = ConfigParser.ConfigParser()
config.read("config.ini")
intern           = mqtt.Client("Mqtt2Mqtt", clean_session=True)
extern           = mqtt.Client("Mqtt2Mqtt", clean_session=True)
extern_connected = False
intern_connected = False


def _on_intern_connect(client, userdata, rc, msg):
    #print ("Connected %s with result code %s" % (client, rc))
    intern_connected = True
    intern.subscribe("#")


def _on_intern_disconnect(client, userdata, msg):
    intern_connected = False
    #print ("Disconnect %s" % client)


def _on_intern_message(client, userdata, msg):
    #print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))
    extern.publish(msg.topic, msg.payload)


def _on_extern_connect(client, userdata, rc, msg):
    #print ("Connected %s with result code %s" % (client, rc))
    #intern.subscribe("#")
    extern_connected = True


def _on_extern_disconnect(client, userdata, msg):
    #print ("Disconnect %s" % client)
    extern_connected = False


def _on_extern_message(client, userdata, msg):
    pass
    #print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))
    #extern.publish(msg.topic, msg.payload)

intern.on_connect    = _on_intern_connect
intern.on_message    = _on_intern_message
intern.on_disconnect = _on_intern_disconnect

extern.username_pw_set(config.get("extern", "user"), config.get("extern", "passwd"))
extern.on_connect    = _on_extern_connect
extern.on_message    = _on_extern_message
extern.on_disconnect = _on_extern_disconnect


while True:

    try:
        if not intern_connected:
            intern.connect(config.get("intern", "host"), int(config.get("intern", "port")))
            intern.loop_start()

        if not extern_connected:
            extern.connect(config.get("extern", "host"), int(config.get("extern", "port")))
            extern.loop_start()
    except Exception as e :
        print e

    time.sleep(10)
