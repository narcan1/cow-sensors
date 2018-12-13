# Legge i valori su udoo e li butta sul db
# gira su udoo, avvia prima cow-db sul server per l'accoglienza API
# leggi valori da udoo e invia API
#
# Sensors device i2c locations:
# barometer: 1-0060, MPL3115A2
# light: 1-0029, TSL2561T
# humidity & temperature: 1-0040, SI7006-A20
#
# I2C sensors values:
# pression [kPa] = x * 0,00025
# light: >1000: fridge light on (to be tested)
# temperature [°C] = x * 0,0625
# temperature and humidity = (raw+offset)*scale/1000

import time
import requests
import json


def main():
    while(True):
        # Calculate Humidity
        f = open("/sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_humidityrelative_raw")
        val = f.read()
        f.close()
        hum_raw = float(val.strip())

        f = open("/sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_humidityrelative_scale")
        val = f.read()
        f.close()
        hum_sca = float(val.strip())

        f = open("/sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_humidityrelative_offset")
        val = f.read()
        f.close()
        hum_off = float(val.strip())

        hum = (hum_raw+hum_off)*hum_sca/1000


        # Calculate Temperature
        f = open("/sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_temp_raw")
        val = f.read()
        f.close()
        tem_raw = float(val.strip())

        f = open("/sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_temp_scale")
        val = f.read()
        f.close()
        tem_sca = float(val.strip())

        f = open("/sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_temp_offset")
        val = f.read()
        f.close()
        tem_off = float(val.strip())

        tem = (tem_raw+tem_off)*tem_sca/1000


        # Calculate Pressure
        f = open("/sys/class/i2c-dev/i2c-1/device/1-0060/iio:device0/in_pressure_raw")
        val = f.read()
        f.close()
        pre_raw = float(val.strip())

        f = open("/sys/class/i2c-dev/i2c-1/device/1-0060/iio:device0/in_pressure_scale")
        val = f.read()
        f.close()
        pre_sca = float(val.strip())

        pre = pre_raw*pre_sca/100


        # Calculate Light
        f = open("/sys/class/i2c-dev/i2c-1/device/1-0029/iio:device1/in_intensity_both_raw")
        val = f.read()
        f.close()
        lig_raw = float(val.strip())

        f = open("/sys/class/i2c-dev/i2c-1/device/1-0029/iio:device1/in_intensity_both_calibscale")
        val = f.read()
        f.close()
        lig_sca = float(val.strip())

        lig = lig_raw*lig_sca/1000

        # prepared to be jsonyfied
        data = {"temperature":tem, "light":lig, "humidity":hum, "pressure":pre}

        try:
            # update_scanner()
            r = requests.put("http://origano.clik.polito.it:8888/api/v1/users/1/scanners/56", data=json.dumps(data))
            print(r.status_code, r.reason)
        except:
            print("Error on API request.")

        time.sleep(1)


if __name__ == "__main__":
    main()

