import bluetooth
import os
import time
from notification import notification
from environment import temperature
class bluetooth_iot:

    @staticmethod
    def search():
        user_name='David'
        device_name='DESKTOP-4KIUH2A'
        while True:
            device_address=None
            dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
            print("\nCurrently: {}".format(dt))
            time.sleep(3) #Sleep three seconds 
            nearby_devices = bluetooth.discover_devices()

            for mac_address in nearby_devices:
                if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                    device_address = mac_address
                    break
            if device_address is not None:
                print("Hi {}! Your phone ({}) has the MAC address: {}".format(user_name, device_name, device_address))
                temp,hum=temperature.measure_temp_hum()
                notification.bluetooth_notification(temp,hum)
                
            else:
                print("Could not find target device nearby...")