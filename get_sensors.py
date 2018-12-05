#girerebbe su udoo
#leggi valori da udoo e chiama la funzione

# Sensors device i2c locations:
# barometer: 1-0060, MPL3115A2
# light: 1-0029, TSL2561T
# humidity & temperature: 1-0040, SI7006-A20


import os, time

while(1):
    # Calculate Humidity
    hum_raw = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_humidityrelative_raw")
    hum_sca = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_humidityrelative_scale")
    hum_off = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0040/iio:device2/in_humidityrelative_offset")
    hum = (hum_raw+hum_off)*hum_sca/1000

    # Calculate Temperature	(to test)
    tem_raw = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0040/iio\:device2/in_temp_raw")
    tem_sca = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0040/iio\:device2/in_temp_scale")
    tem_off = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0040/iio\:device2/in_temp_offset")
    tem = (tem_raw+tem_off)*tem_sca/1000

    # Calculate Pressure (to test)
    pre_raw = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0060/iio\:device0/in_pressure_raw")
    pre_sca = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0060/iio\:device0/in_pressure_scale")
    #Is there another value?
    #?

    # Calculate Light (to test)
    lig_raw = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0029/iio\:device1/in_intensity_both_raw")
    lig_off = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0029/iio\:device1/in_intensity_both_offset")
    lig_sca = os.system("cat /sys/class/i2c-dev/i2c-1/device/1-0029/iio\:device1/in_intensity_both_scale")
    lig = (lig_raw+lig_off)*lig_sca/1000

    data = {"temperature":"tem", "light":"lig", "humidity":"hum", "pressure":"pre"}     #json? prova senza graffe

    try:        #rivedi codice API
        #('/api/v1/users/<user_id>/scanners/<scanner_id>', methods=['PUT'])
        r = requests.post("http://origano.clik.polito.it:8888/api/v1/users/1/scanners/56", data=data)
    except:
        print("Error on API request.")

    # UDOO sensors
    # pression [kPa] = x * 0,00025
    # light: >1000: fridge light on (to be tested)
    # temperature [°C] = x * 0,0625
    # temperature and humidity = (raw+offset)*scale/1000

    time.sleep(1)
