# Homie v4 implementation for Python ~3.8

A fork of the Python 3 implementation of Homie 4.0.0. by mjcumming.

**Install**

```
pip install git+https://github.com/juusokorhonen/Homie4
```

**Gateway Example**

```python

from homie.device_gateway import Device_Gateway

```

**Temperature Probe Example**

Creates a temperature device using a AM2302 sensor.

```python
import Adafruit_DHT
import time

from homie.device_temperature import Device_Temperature

mqtt_settings = {
    'MQTT_BROKER' : 'localhost',
    'MQTT_PORT' : 1883,
}

try:

    temperature_device = Device_Temperature(device_id="temperature-sensor-1",name = "Temperature_Sensor 1",mqtt_settings=mqtt_settings)
    sensor = Adafruit_DHT.AM2302
    pin = 4


    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print(temperature)
        temperature_device.update_temperature(temperature)
        time.sleep(5)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")
```

**Dimmer Example**

To create a dimmer device requires that a set_dimmer method be provided. When creating a device, all that is required is to provide the MQTT settings. All other requirements of the Homie specification are automatically handled.

```python
import time

from homie.device_dimmer import Device_Dimmer

mqtt_settings = {
    'MQTT_BROKER' : 'localhost',
    'MQTT_PORT' : 1883,
}

class My_Dimmer(Device_Dimmer):

    def set_dimmer(self,percent):
        print('Received MQTT message to set the dimmer to {}. Must replace this method'.format(percent))
        super().set_dimmer(percent)

try:

    dimmer = My_Dimmer(name = 'Test Dimmer',mqtt_settings=mqtt_settings)

    while True:
        dimmer.update_dimmer(0)
        time.sleep(5)
        dimmer.update_dimmer(50)
        time.sleep(5)
        dimmer.update_dimmer(100)
        time.sleep(5)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")


```

If creating multiple homie devices, you can specify Homie to only use one MQTT connection. This can be an issue on devices with limited resources. For MQTT_SETTINGS add MQTT_SHARE_CLIENT: True.
