#Install Dockercontainers

#Install mqtt gateway
```bash
git clone https://github.com/AnsgarSchmidt/EpicFabLabWeather.git
cd EpicFabLabWeather/Dashboard
virtualenv .
. bin/activate
pip install -r requirements.txt
cp config.ini-default config.ini
```
Edit your config.ini file
```bash
sudo cp mqtt2mqtt /etc/init.d/
sudo update-rc.d mqtt2mqtt defaults
```
