'''
This Example sends harcoded data to Ubidots using the request HTTP
library.

Please install the library using pip install requests

Made by Jose García @https://github.com/jotathebest/
'''

import string
from tkinter.tix import INTEGER
import requests
import time

'''
global variables
'''
ENDPOINT = "things.ubidots.com" 
DEVICE_LABEL = "box-viewer" #
VARIABLE_LABEL = "boxContent"
#BBFF-NOPYPdeXHpXRzhEWBpQlBbl5ErAgoQ
TOKEN = "BBFF-NOPYPdeXHpXRzhEWBpQlBbl5ErAgoQ" # replace with your TOKEN
sensor_value = None
light_or_dark = 1

def post_var(payload, url=ENDPOINT, device=DEVICE_LABEL, token=TOKEN):
    try:
        # url = "http://{}/api/v1.6/devices/{}".format(url, device)
        url = "http://things.ubidots.com/api/v1.6/devices/box-viewer" 
        headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

        status_code = 400

        if status_code >= 400:
            #print("[INFO] Sending data, attempt number: {}".format(attempts))
            req = requests.post(url=url, headers=headers, json=payload)
            status_code = req.status_code
            time.sleep(1)

        #print("[INFO] Results:")
        #print(req.text)
    except Exception as e:
        print("[ERROR] Error posting, details: {}".format(e))

def make_str(str_id):
    re_str = ""
    for item in  str_id:
        re_str +=  str(item)+" "
    return re_str

def upload_ID(str_id):
    global sensor_value
    global light_or_dark
    # Simulates sensor values
    ss = make_str(str_id)
    #payload = {VARIABLE_LABEL: light_or_dark}
    payload = {VARIABLE_LABEL : {"value" : 0 , "context" : {"id" : ss}}}
    post_var(payload)