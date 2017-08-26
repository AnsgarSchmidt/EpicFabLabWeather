import time
import grovepi
import paho.mqtt.client as mqtt
import grove_i2c_digital_light_sensor


def _on_connect(client, userdata, rc, msg):
    print ("Connected %s with result code %s" % (client, rc))
    mymqtt.subscribe("buzzer")


def _on_disconnect(client, userdata, msg):
    print ("Disconnect %s" % client)


def _on_message(client, userdata, msg):
    print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))
    # do the buzz here

def init_sensors():
    grove_i2c_digital_light_sensor.init()

def publish_light_data():
    try:
        data = grove_i2c_digital_light_sensor.readVisibleLux()
        mymqtt.publish("phalanx/light_sensor", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)


def publish_uv_data():
    try:
        uv_sensor=1
	data = grovepi.analogRead(uv_sensor)
        mymqtt.publish("phalanx/uv_sensor", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)

def publish_temperature_data():
    try:
        temperature_sensor=2
        data = grovepi.analogRead(temperature_sensor)
        mymqtt.publish("phalanx/temperature_sensor", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)

def publish_water_data():
    try:
        water_sensor=3
	data = grovepi.analogRead(water_sensor)
        mymqtt.publish("phalanx/water_sensor",data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)

def publish_ir_data():
    try:
	ir_sensor=5
	data = grovepi.analogRead(ir_sensor)
        mymqtt.publish("phalanx/ir_movement_sensor", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)

mymqtt = mqtt.Client("sensors", clean_session=True)
mymqtt.on_connect    = _on_connect
mymqtt.on_message    = _on_message
mymqtt.on_disconnect = _on_disconnect
mymqtt.connect("172.26.2.9", 1883)
mymqtt.loop_start()

init_sensors()
while True:
    try:
	publish_light_data()
	publish_uv_data()
	publish_temperature_data()
	publish_water_data()
	publish_ir_data()

        time.sleep(10)
    except KeyboardInterrupt:
        break
    except:
        print ("Unexpected Error" + sys.exc_info()[0])
