import time
import json
import requests
import threading
import ConfigParser


class OpenWeatherMap(threading.Thread):

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
            print "error:%s" % key
            return 0.0

    def _sendData(self):
        url = "http://api.openweathermap.org/data/3.0/measurements?appid=%s" % self._config.get("OpenWeatherMap", "appid")
        data = [{
                "station_id": self._config.get("OpenWeatherMap", "stationid"),
                "dt": int(time.time()),
                "temperature": self._getData("davis/outTemp_C"),
                "wind_speed": self._getData("davis/windSpeed_kph") * 0.277778,
                "wind_gust": self._getData("davis/windGust_kph") * 0.277778,
                "wind_deg": self._getData("davis/windDir"),
                "pressure": self._getData("davis/barometer_mbar"),
                "humidity": self._getData("davis/outHumidity"),
                "rain_1h": self._getData("davis/rain_cm") * 10,
                "rain_24h": self._getData("davis/dayRain_cm") * 10,
                "dew_point": self._getData("davis/dewpoint_C"),
                "humidex": self._getData("davis/humidex_C"),
                "head_index": self._getData("davis/heatindex_C")
               }]

        #print json.dumps(data, indent=4, sort_keys=True)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print response

    def run(self):
        time.sleep(60)
        while True:
            self._sendData()
            time.sleep(15)
