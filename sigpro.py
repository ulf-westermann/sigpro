import argparse
import signal

import driver_serial_metex_14_byte
import driver_usbhid_brymen_bm86x


def signal_handler(sig, frame):
    driver.close()


def on_acquisition(timestamp: float, analog_channels: None|list[None|list[float, str], ...], digital_channels: None|list[None|float] = None):
    print(f"on_acquisition. timestamp: {timestamp}, analog channels: {analog_channels}, digital channels: {digital_channels}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="sigpro", description="Signal Processing")
    parser.add_argument("-y", "--tty", help="tty device", type=str, default="/dev/ttyUSB0")
    parser.add_argument("-b", "--baudrate", help="baud rate", type=int, default=9600)
    parser.add_argument("-a", "--databits", help="number of data bits", type=int, choices=[5, 6, 7, 8], default=7)
    parser.add_argument("-p", "--parity", help="parity", type=str, choices=["o", "e", "n"], default="n")
    parser.add_argument("-s", "--stopbits", help="number of stop bits", type=int, choices=[1, 2], default=2)
    parser.add_argument("-r", "--rtscts", help="hardware flow control", action="store_true", default=False)
    parser.add_argument("-t", "--dtrdsr", help="use dtr/dsr", action="store_true", default=False)
    parser.add_argument("driver", help="name of driver", type=str, choices=["brymen86", "metex14"], default="brymen86")
    args = parser.parse_args()

    if args.driver == "metex14":
        driver = driver_serial_metex_14_byte.DriverSerialMetex14Byte(on_acquisition, 0, device=args.tty,
                                                                     baudrate=args.baudrate, databits=args.databits, parity=args.parity.upper(),
                                                                     stopbits=args.stopbits, rtscts=args.rtscts, dtrdsr=args.dtrdsr)
    elif args.driver == "brymen86":
        driver = driver_usbhid_brymen_bm86x.DriverUsbHidBrymenBm86x(on_acquisition, 0)

    signal.signal(signal.SIGINT, signal_handler)
