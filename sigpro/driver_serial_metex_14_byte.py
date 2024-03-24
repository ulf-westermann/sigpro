import datetime
import time
import typing

import driver_serial_base


class DriverSerialMetex14Byte(driver_serial_base.DriverSerialBase):
    def __init__(self, acquisition_callback: typing.Callable, acquisition_interval_millis: int, **kwargs):
        self.acquisition_callback = acquisition_callback
        self.acquisition_interval_millis = acquisition_interval_millis / 1000

        super().__init__(**kwargs)

    def convert_to_channel(self, acquired_data: bytes) -> None | list[float, str]:
        #print(f"acquired data: <{acquired_data}>")
        if len(acquired_data) < 14:
            return None
        text = acquired_data.decode(encoding="ascii")[-14:-1]
        #print(f"text <{text}>, len: {len(text)}")
        analog_value = text[3:10].strip()
        analog_unit = text[:3].strip() + " " + text[10:].strip()
        return [analog_value, analog_unit]

    def init_acquisition(self):
        self.serial.timeout = 2
        self.serial.write_timeout = None
        self.serial.setRTS(False)
        self.next_acquisition_time = None

    def acquire_data(self):
        now = time.time()

        if self.acquisition_interval_millis > 0:
            if not self.next_acquisition_time:
                self.next_acquisition_time = now

            if self.next_acquisition_time > now:
                time.sleep(0.001)
                return

            #print(f"acquisition: current acquisition time: {self.next_acquisition_time}, now: {now}")

        # dummy read to empty buffer
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()

        self.send("D".encode(encoding="ascii"))

        analog1 = self.convert_to_channel(self.serial.read_until(b"\r"))
        analog2 = self.convert_to_channel(self.serial.read_until(b"\r"))
        analog3 = self.convert_to_channel(self.serial.read_until(b"\r"))
        analog4 = self.convert_to_channel(self.serial.read_until(b"\r"))

        self.acquisition_callback(now, [analog1, analog2, analog3, analog4])

        time.sleep(0.1) # too fast repetition creates problems in some modes

        if self.acquisition_interval_millis > 0:
            self.next_acquisition_time += self.acquisition_interval_millis

            #print(f"next acquisition: time: {self.next_acquisition_time}, now: {time.time()}")

            while self.next_acquisition_time < time.time():
                self.acquisition_callback(self.next_acquisition_time, None, None)
                self.next_acquisition_time += self.acquisition_interval_millis
                #print(f"next acquisition deadline missed, adding extra interval, next acquisition is now at {self.next_acquisition_time}")
