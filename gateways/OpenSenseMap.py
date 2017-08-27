# -*- coding: utf-8 -*-
import time
import json
import requests
import threading
import ConfigParser

class OpenSenseMap(threading.Thread):

    def _createRequestBody(self, sensor):
        post_url = "https://api.opensensemap.org/boxes/" + self._config.get("OpenSenseMap", "sensebox_id") + "/" + self._config.get("OpenSenseMap", sensor)
        #print "SENSOR " + self._config.get("OpenSenseMap", sensor)
        #print "DAVIS " + self._config.get("Davis", sensor)
        #print "URL " + post_url
        data = []
        if sensor in ["wind_speed", "wind_direction"]:
            data = {
                "value": self._getData(self._config.get("Davis", sensor)) * 0.277778
            }
        elif sensor in ["rain_1h", "rain_24h"]:
            data = {
                "value": self._getData(self._config.get("Davis", sensor)) * 10
            }
        else:
            data = {
                "value": self._getData(self._config.get("Davis", sensor))
            }
        #print "DATA " + str(data)
        return post_url, data

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._data = data
        self._config = ConfigParser.ConfigParser()
        self._config.read("config.ini")

    def _getData(self, key):
        if key in self._data:
            return float(self._data[key])
        else:
            #print "error:%s" % key
            return 0.0

    def _sendData(self):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        for sensor in ["temperature", "wind_speed", "wind_gust", "wind_direction", "pressure", "humidity", "rain_1h", "rain_24h", "dew_point", "humidex", "heat_index"]:
            post_url, data = self._createRequestBody(sensor);
            response = (requests.post(post_url, data=json.dumps(data), headers=headers)).text
            #print response

    def run(self):
        time.sleep(60)
        while True:
            #print "+++++++KEYS++++++++"
            #print self._data.keys()
            self._sendData()
            time.sleep(15)
