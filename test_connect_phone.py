import uiautomator2 as u2
import time


def connect_phone(device_serial: str = None):
    if device_serial:
        d = u2.connect(device_serial)
    else:
        d = u2.connect()

    print(f"Connected to device: {d.info['productName']}")
    print(f"Device serial: {d.serial}")

    return d


if __name__ == "__main__":
    print("Starting uiautomator2 auto-connect demo...")

    try:
        device = connect_phone()
        print("\nConnection successful!")
        
        device.set_input_ime(True)
        login_mobile_number_input = device.xpath('//*[@resource-id="com.lphtsccft:id/login_mobile_number_input"]')
        login_mobile_number_input.click()
        device.clear_text()
        device.sleep(1)
        login_mobile_number_input.set_text("12345678901")
        device.set_input_ime(False)
    except Exception as e:
        print(f"Connection failed: {e}")
