import traceback
import threading

import hid


class DriverUsbHidBase(threading.Thread):
    def __init__(self, id_vendor: int, id_product: int):
        super().__init__()

        self.device = hid.device()

        self.stop = False
        self.start()

    def close(self):
        self.stop = True
        self.join()
        self.device.close()

    def send(self, data: bytes):
        self.device.write(data)

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
