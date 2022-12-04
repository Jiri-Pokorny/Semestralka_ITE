import time
import machine
import onewire, ds18x20
import sys

class Thermometer:

    def __init__(self) -> None:
        print("Thermometer - init...")
        self.dat = machine.Pin(5)
        self.ds = ds18x20.DS18X20(onewire.OneWire(self.dat))
        try:
            # scan for devices on the bus
            self.roms = self.ds.scan()
            print('found devices:', self.roms)
        except Exception:
            machine.reset()

    def measure(self):
        print("Thermometer - measure...")
        try:
            self.ds.convert_temp()
            time.sleep_ms(750)
            temp = 0
            for rom in self.roms:
                temp = self.ds.read_temp(rom)
            return temp
        except Exception:
            machine.reset()




