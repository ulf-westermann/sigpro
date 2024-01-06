import time
import typing

import driver_usbhid_base


class DriverUsbHidBrymenBm86x(driver_usbhid_base.DriverUsbHidBase):
    def __init__(self, acquisition_callback: typing.Callable, acquisition_interval_millis: int):
        self.acquisition_callback = acquisition_callback
        self.acquisition_interval_millis = acquisition_interval_millis / 1000

        super().__init__(0x820, 0x1)

    def read_channels(self) -> bytes:
        bytes_remaining = 27 - 3
        report = bytearray()
        while bytes_remaining > 0:
            data = self.device.read(bytes_remaining, timeout_ms=4000)
            bytes_returned = len(data)
            if bytes_returned == 0:
                break
            report.extend(data)
            bytes_remaining -= len(data)

        return report

    def acquire_data(self):
        now = time.time()

        if self.acquisition_interval_millis > 0:
            if not self.next_acquisition_time:
                self.next_acquisition_time = now

            if self.next_acquisition_time > now:
                time.sleep(0.001)
                return

        self.device.open(0x820, 1)
        self.device.set_nonblocking(False)
        self.send(bytes([0, 0, 0x86, 0x66]))

        report = self.read_channels()
        print(report)

        self.device.close()

        #self.acquisition_callback(now, [analog1, analog2, analog3, analog4])

        #time.sleep(0.1) # too fast repetition creates problems in some modes

        if self.acquisition_interval_millis > 0:
            self.next_acquisition_time += self.acquisition_interval_millis

            while self.next_acquisition_time < time.time():
                self.acquisition_callback(self.next_acquisition_time, None, None)
                self.next_acquisition_time += self.acquisition_interval_millis
