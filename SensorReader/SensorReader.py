import sys
import json
import time
import base64
import requests
import grovepi
import paho.mqtt.client as mqtt
from grove_i2c_digital_light_sensor import Tsl2561
import grove_i2c_digital_light_sensor

# phalanx/buzzer <------ IN

# phalanx/noise
# phalanx/uv
# phalanx/ir
# phalanx/visible_light
# phalanx/leaf
# phalanx/particulate_matter_10
# phalanx/particulate_matter_2_5
# phalanx/dust
# phalanx/temperature
# phalanx/humidity
# phalanx/tamper
# phalanx/pir


def _on_connect(client, userdata, rc, msg):
    print ("Connected %s with result code %s" % (client, rc))
    mymqtt.subscribe("buzzer")


def _on_disconnect(client, userdata, msg):
    print ("Disconnect %s" % client)


def _on_message(client, userdata, msg):
    print("Mq Received on channel %s -> %s" % (msg.topic, msg.payload))
    # do the buzz here

def init_sensors():
    global TSL2561
    TSL2561 = Tsl2561()
    TSL2561._init__(grove_i2c_digital_light_sensor.I2C_SMBUS, grove_i2c_digital_light_sensor.I2C_ADDRESS)
    #grove_i2c_digital_light_sensor.init()


def send_image():
    with open("/tmp/webcam.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
        mymqtt.publish("phalanx/image", encoded)


def publish_light_data():
    try:
        gain = 0
        val = TSL2561.readLux(gain)
        ambient = val[0]
        IR = val[1]
        _ambient = val[2]
        _IR = val[3]
        _LUX = val[4]
        mymqtt.publish("phalanx/visible_light", _LUX)
        mymqtt.publish("phalanx/ir", IR)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)


def publish_uv_data():
    try:
        uv_sensor = 1
        data = grovepi.analogRead(uv_sensor)
        mymqtt.publish("phalanx/uv", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)


def publish_temperature_data():
    try:
        temperature_sensor = 2
        data = float(grovepi.analogRead(temperature_sensor)) / 10
        mymqtt.publish("phalanx/temperature", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)

def publish_humidity_data():
    try:
        dht_sensor = 4
        [temp,humidity] = grovepi.dht(dht_sensor, 1)
        mymqtt.publish("phalanx/humidity", humidity)
        print ("temp =" + str(temp) +  " humidity =" + str(humidity))
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)


def publish_water_data():
    try:
        water_sensor = 3
        data = 1023 - grovepi.analogRead(water_sensor)
        mymqtt.publish("phalanx/leaf",data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)


def publish_pir_data():
    try:
        pir_movement_sensor = 8
        data = grovepi.digitalRead(pir_movement_sensor)
        if data == 0 or data == 1: # check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
            mymqtt.publish("phalanx/pir", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)

def publish_noise_data():
    try:
        noise_sensor=0
        data = grovepi.analogRead(noise_sensor)
        mymqtt.publish("phalanx/noise", data)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)


def publish_particulate_matter():
    try:
        p1      = 0.0
        p2      = 0.0
        counter = 0
        data    = json.loads(requests.get("http://api.luftdaten.info/v1/sensor/4337/").content)
        if data is not None:
            for entry in data:
                # print json.dumps(entry, indent=4, sort_keys=True)
                for sensor in entry['sensordatavalues']:
                    if sensor['value_type'] == "P1":
                        p1 += float(sensor['value'])
                    if sensor['value_type'] == "P2":
                        p2 += float(sensor['value'])
                counter += 1
            p1 /= counter
            p2 /= counter
            p1 = float("{0:.2f}".format(p1))
            p2 = float("{0:.2f}".format(p2))
            mymqtt.publish("phalanx/particulate_matter_10", p1)
            mymqtt.publish("phalanx/particulate_matter_2_5", p2)
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)


def publish_detected_airplanes():
    try:
        data = json.loads(requests.get("http://localhost:8754/flights.json").content)
        if data is not None:
            #print json.dumps(data, indent=4, sort_keys=True)
            mymqtt.publish("phalanx/detected_airplanes", len(data))
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
        publish_noise_data()
        publish_uv_data()
        publish_light_data()
        publish_water_data()
        publish_temperature_data()
	publish_humidity_data()
        publish_particulate_matter()
        publish_detected_airplanes()
        publish_pir_data()
        send_image()
        time.sleep(10)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print ("Unexpected Error %s" + str(sys.exc_info()[0]))
        time.sleep(100)
