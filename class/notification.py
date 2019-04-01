import os
import requests
import json
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
           
    @staticmethod
    def execute_notification():
        ip_address = os.popen('hostname -I').read()
        notification.send_notification_via_pushbullet(ip_address, "The temperature or the humidity is out of the range")
