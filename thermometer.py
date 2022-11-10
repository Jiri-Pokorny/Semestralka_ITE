import time
import machine
import onewire, ds18x20
import sys
import logger

# the device is on GPIO12
dat = machine.Pin(5)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
roms = ds.scan()
print('found devices:', roms)

def measure():
    try:
        ds.convert_temp()
        time.sleep_ms(750)
        temp = 0
        for rom in roms:
            temp = ds.read_temp(rom)
        return temp
    except Excepton as e:
        logger.log("Thermometer exception: ", e)
        sys.exit()