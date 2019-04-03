# import packages
import requests
import os
import json
from db import database

class notification:

    @staticmethod
    def send_notification_via_pushbullet(title, body):
        """ Sending notification via pushbullet.
        Args:
        title (str) : title of text.
        body (str) : Body of text.
        """
        ACCESS_TOKEN="o.w75BDnf5ujJdrsQ15ZcjFB3je03NEn3C"
        data_send = {"type": "note", "title": title, "body": body}
        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Something wrong')
        else:
            print('complete sending')
           
    # This function either sends notification or print a message
    # stating that a message has been sent today
    @staticmethod
    def execute_notification():
        # call getNotificationTimes function from database which return either 0 or 1
        # if it returns 1, then that means that a notification has not been sent today
        check = database.getNotificationTimes()
        if check == 1:
            # send a notifiaction 
            ip_address = os.popen('hostname -I').read()
            # specified a message to display in the device we're sending notification to
            notification.send_notification_via_pushbullet(ip_address, "The temperature or the humidity is out of the range")
            # insert the current date when we send a notification to the notification table
            # so that we don't send a notification again in that date
            # this can be accomplished by calling insertNotificationTime function from database class
            database.insertNotificationTime()
            # database.insertIntoTable('NOTIFICATION_data')
        # if returns 0, that means a message has already been sent today.
        # So we print a message
        else:
            print('Notification has been sent today!')
    @staticmethod
    def bluetooth_notification(temp,hum):
        check = database.getBluetoothNotificationTimes()
        ip_address = os.popen('hostname -I').read()
        if check == 1:
            ip_address=os.popen('hostname -I').read()
            str='The tempreture is ? The humidity is ?',(temp,hum)
            notification.send_notification_via_pushbullet(ip_address,str)
            database.insertBluetoothNotificationTime()
            # database.insertIntoTable('BLUETOOTH_notification')
        else:
            print('Bluetooth Notification has been sent today!')

