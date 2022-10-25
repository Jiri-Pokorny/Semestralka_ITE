import time
import machine
import onewire, ds18x20


# the device is on GPIO12
dat = machine.Pin(5)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
roms = ds.scan()
print('found devices:', roms)

def measure():
    ds.convert_temp()
    time.sleep_ms(750)
    temp = 0
    for rom in roms:
        temp = ds.read_temp(rom)
    return temp
'''
for i in range(5):
    tmp = measure()
    print("Measured: ", tmp)'''