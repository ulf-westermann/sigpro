import traceback
import threading

import serial


class DriverSerialBase(threading.Thread):
    def __init__(self, device: str, baudrate: int, databits: int, parity: str, stopbits: int, rtscts: bool, dtrdsr: bool):
        super().__init__()

        self.serial = serial.Serial(device, baudrate=baudrate, bytesize=databits, parity=parity, stopbits=stopbits,
                                    rtscts=rtscts, dsrdtr=dtrdsr)
        self.stop = False
        self.start()

    def close(self):
        self.stop = True
        self.join()
        self.serial.close()

    def send(self, data: bytes):
        self.serial.write(data)

    def run(self):
        try:
            self.init_acquisition()
            while not self.stop:
                self.acquire_data()
        except:
            traceback.print_exc()

    def init_acquisition(self):
        pass

    def acquire_data(self):
        pass
