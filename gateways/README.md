# setup
````bash
cd EpicFabLabWeather/gateways
virtualenv .
. bin/activate
pip install -r requirements.txt
cp config.ini-defaults config.ini
````

Configure config.ini

```bash
sudo cp opendatagateways /etc/init.d/
sudo update-rc.d opendatagateways defaults
```
