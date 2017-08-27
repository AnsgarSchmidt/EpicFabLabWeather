var app = require('../server/app');

// Configure Fablab 
var weather = new app.Dictionary('Weather', 'Weather');

weather.addMeasurement('OutHumidity', 'weather.outhumidity', [
  {
    units: '%',
    format: 'float',
    min: 10,
    max: 100
  }
], {
  topic: 'davis/outHumidity'
});


weather.addMeasurement('InHumidity', 'weather.inhumidity', [
  {
    units: '%',
    format: 'float',
    min: 10,
    max: 100
  }
], {
  topic: 'davis/inHumidity'
});


weather.addMeasurement('Pressure', 'weather.pressure', [
  {
    units: 'mBar',
    format: 'float',
    min: 900,
    max: 1100
  }
], {
  topic: 'davis/pressure_mbar'
});


weather.addMeasurement('Rain', 'weather.rain', [
  {
    units: 'cm',
    format: 'float',
    min: 0,
    max: 2
  }
], {
  topic: 'davis/rain_cm'
});


weather.addMeasurement('Battery', 'weather.battery', [
  {
    units: 'Volt',
    format: 'float',
    min: 4,
    max: 6
  }
], {
  topic: 'davis/consBatteryVoltage_volt'
});


weather.addMeasurement('OutDewPoint', 'weather.outdewpoint', [
  {
    units: 'Celcius',
    format: 'float',
    min: -10,
    max: 30
  }
], {
  topic: 'davis/dewpoint_C'
});


weather.addMeasurement('InDewPoint', 'weather.indewpoint', [
  {
    units: 'Celcius',
    format: 'float',
    min: 10,
    max: 30
  }
], {
  topic: 'davis/inDewpoint'
});


weather.addMeasurement('Heatindex', 'weather.heatindex', [
  {
    units: 'Celcius',
    format: 'float',
    min: -10,
    max: 40
  }
], {
  topic: 'davis/heatindex_C'
});


weather.addMeasurement('Windspeed', 'weather.windspeed', [
  {
    units: 'km/h',
    format: 'float',
    min: 0,
    max: 50
  }
], {
  topic: 'davis/windSpeed_kph'
});


weather.addMeasurement('WindDir', 'weather.winddir', [
  {
    units: 'Degrees',
    format: 'float',
    min: 0,
    max: 360
  }
], {
  topic: 'davis/windDir'
});


weather.addMeasurement('Gustspeed', 'weather.gustspeed', [
  {
    units: 'km/h',
    format: 'float',
    min: 0,
    max: 50
  }
], {
  topic: 'davis/windGust_kph'
});


weather.addMeasurement('GustDir', 'weather.gustdir', [
  {
    units: 'Degrees',
    format: 'float',
    min: 0,
    max: 360
  }
], {
  topic: 'davis/windGustDir'
});


weather.addMeasurement('InTemp', 'weather.intemp', [
  {
    units: 'Celcius',
    format: 'float',
    min: 10,
    max: 50
  }
], {
  topic: 'davis/inTemp_C'
});


weather.addMeasurement('OutTemp', 'weather.outtemp', [
  {
    units: 'Celcius',
    format: 'float',
    min: -10,
    max: 50
  }
], {
  topic: 'davis/outTemp_C'
});


// Start the server
var server = new app.Server({
  host: process.env.HOST || 'localhost',
  port: process.env.PORT || 8080,
  wss_port: process.env.WSS_PORT || 8082,
  broker: process.env.MSGFLO_BROKER || 'mqtt://c-beam.cbrp3.c-base.org',
  dictionaries: [
    weather
  ],
  theme: 'Snow',
  history: {
    host: process.env.INFLUX_HOST || 'localhost',
    db: process.env.INFLUX_DB || 'cbeam'
  }//,
  //persistence: 'openmct.plugins.CouchDB("http://openmct.cbrp3.c-base.org:5984/openmct")'
});
server.start(function (err) {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log('Server listening in ' + server.config.port);
});
