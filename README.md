# C.O.W. Sensors software

This software is part of the project **"C.O.W. (Cut Off Waste)"**, born during an hackathon about *"Smart Packaging and Sustainability"* at the CLab *"CLIK"* in Polytechnic of Turin.
It is written in Python 3.x and uses sensors connected via I2C to monitorate the status of the fridge.

## Sensors

`/sys/class/i2c-dev/i2c-1/device/<device_no>/iio:device0/`

* barometer: 1-0060, MPL3115A2

* light: 1-0029, TSL2561T

* humidity & temperature: 1-0040, SI7006-A20

