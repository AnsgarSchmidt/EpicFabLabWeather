import time
import urllib
import requests
import threading
import ConfigParser
from datetime import datetime


class Wunderground(threading.Thread):

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
            print "wundererrrorkey:%s" % key
            return 0.0

    def _sendData(self):
        url = "http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php"
        url += "?ID=%s" % self._config.get("Wunderground", "id")
        url += "&PASSWORD=%s" % self._config.get("Wunderground", "passwd")
        url += "&action=updateraw"
        url += "&dateutc=%s"        % urllib.quote(str(datetime.utcnow()).split(".")[0])
        url += "&winddir=%f"        %   self._getData('davis/windDir'                 )
        url += "&windspeedmph=%f"   % ( self._getData('davis/windSpeed_kph'           ) * 0.621371)
        url += "&windgustmph=%f"    % ( self._getData('davis/windGust_kph'            ) * 0.621371)
        url += "&windgustdir=%f"    %   self._getData('davis/windGustDir'             )
        url += "&humidity=%f"       %   self._getData('davis/outHumidity'             )
        url += "&dewptf=%f"         % ((self._getData('davis/dewpoint_C'              ) * (9.0/5.0)) + 32)
        url += "&tempf=%f"          % ((self._getData('davis/outTemp_C'               ) * (9.0/5.0)) + 32)
        url += "&rainin=%f"         % ( self._getData('davis/hourRain_cm'             ) * 0.393701)
        url += "&dailyrainin=%f"    % ( self._getData('davis/dayRain_cm'              ) * 0.393701)
        url += "&baromin=%f"        % ( self._getData('davis/barometer_mbar'          ) * 0.0145038)
        url += "&indoortempf=%f"    % ((self._getData('davis/inTemp_C'                ) * (9.0/5.0)) + 32)
        url += "&indoorhumidity=%f" %   self._getData('davis/inHumidity'              )
        url += "&AqPM2.5=%f"        %   self._getData('phalanx/particulate_matter_2_5')
        url += "&leafwetness=%f"    %   self._getData('phalanx/leaf'                  )
        url += "&UV=%f"             % ((self._getData('phalanx/uv'                    ) - 60) / 10.0)
        url += "&solarradiation=%f" %   self._getData('phalanx/light_sensor'          )
        url += "&realtime=1"
        url += "&rtfreq=15"
        url += "&softwaretype=EpicFabLabWeather"

        #print url
        response = requests.get(url).content
        print response

    def run(self):

        time.sleep(60)
        while True:
            self._sendData()
            time.sleep(15)
