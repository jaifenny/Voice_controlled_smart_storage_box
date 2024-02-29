#物聯網專題，抓取ubidots資訊，並傳送到LINE
from flask import Flask
app = Flask(__name__)

from flask import Flask, request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, TextMessage

import requests #做post請求
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# LINE bot 設定
line_bot_api = LineBotApi('ixlul69vBBiqft1YoOwtiBYmVmTwqZIJJR06N8ns/MJ4B3/ogUd5OKnsC12TYB31l/e3a/N4Q7H5qjJo2nNaqDeho/ApjKdFt00CazHazMcYZtnq3YTZ2r83Ic/KEAazrFgvC0o8a96xpF7FqxE4UAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('43514f67a4b3eed59c011e1937de86d9')

# ubidots設定
ENDPOINT = "things.ubidots.com"
DEVICE_LABEL = "box-viewer"  #me
VARIABLE_LABEL = "boxContent"  #me
TOKEN = "BBFF-NOPYPdeXHpXRzhEWBpQlBbl5ErAgoQ" # replace with your TOKEN  #me
DELAY = 0.1  # Delay in seconds
URL = "http://{}/api/v1.6/devices/{}/{}/?page_size=1".format(ENDPOINT, DEVICE_LABEL, VARIABLE_LABEL) #網址    #me
HEADERS = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

category = {1: {'id': 1, 'name': 'person'}, 2: {'id': 2, 'name': 'bicycle'}, 3: {'id': 3, 'name': 'car'}, 4: {'id': 4, 'name': 'motorcycle'}, 5: {'id': 5, 'name': 'airplane'}, 6: {'id': 6, 'name': 'bus'}, 7: {'id': 7, 'name': 'train'}, 8: {'id': 8, 'name': 'truck'}, 9: {'id': 9, 'name': 'boat'}, 10: {'id': 10, 'name': 'traffic light'}, 11: {'id': 11, 'name': 'fire hydrant'}, 13: {'id': 13, 'name': 'stop sign'}, 14: {'id': 14, 'name': 'parking meter'}, 15: {'id': 15, 'name': 'bench'}, 16: {'id': 16, 'name': 'bird'}, 17: {'id': 17, 'name': 'cat'}, 18: {'id': 18, 'name': 'dog'}, 19: {'id': 19, 'name': 'horse'}, 20: {'id': 20, 'name': 'sheep'}, 21: {'id': 21, 'name': 'cow'}, 22: {'id': 22, 'name': 'elephant'}, 23: {'id': 23, 'name': 'bear'}, 24: {'id': 24, 'name': 'zebra'}, 25: {'id': 25, 'name': 'giraffe'}, 27: {'id': 27, 'name': 'backpack'}, 28: {'id': 28, 'name': 'umbrella'}, 31: {'id': 31, 'name': 'handbag'}, 32: {'id': 32, 'name': 'tie'}, 33: {'id': 33, 'name': 'suitcase'}, 34: {'id': 34, 'name': 'frisbee'}, 35: {'id': 35, 'name': 'skis'}, 36: {'id': 36, 'name': 'snowboard'}, 37: {'id': 37, 'name': 'sports ball'}, 38: {'id': 38, 'name': 'kite'}, 39: {'id': 39, 'name': 'baseball bat'}, 40: {'id': 40, 'name': 'baseball glove'}, 41: {'id': 41, 'name': 'skateboard'}, 42: {'id': 42, 'name': 'surfboard'}, 43: {'id': 43, 'name': 'tennis racket'}, 44: {'id': 44, 'name': 'bottle'}, 46: {'id': 46, 'name': 'wine glass'}, 47: {'id': 47, 'name': 'cup'}, 48: {'id': 48, 'name': 'fork'}, 49: {'id': 49, 'name': 'knife'}, 50: {'id': 50, 'name': 'spoon'}, 51: {'id': 51, 'name': 'bowl'}, 52: {'id': 52, 'name': 'banana'}, 53: {'id': 53, 'name': 'apple'}, 54: {'id': 54, 'name': 'sandwich'}, 55: {'id': 55, 'name': 'orange'}, 56: {'id': 56, 'name': 'broccoli'}, 57: {'id': 57, 'name': 'carrot'}, 58: {'id': 58, 'name': 'hot dog'}, 59: {'id': 59, 'name': 'pizza'}, 60: {'id': 60, 'name': 'donut'}, 61: {'id': 61, 'name': 'cake'}, 62: {'id': 62, 'name': 'chair'}, 63: {'id': 63, 'name': 'couch'}, 64: {'id': 64, 'name': 'potted plant'}, 65: {'id': 65, 'name': 'bed'}, 67: {'id': 67, 'name': 'dining table'}, 70: {'id': 70, 'name': 'toilet'}, 72: {'id': 72, 'name': 'tv'}, 73: {'id': 73, 'name': 'laptop'}, 74: {'id': 74, 'name': 'mouse'}, 75: {'id': 75, 'name': 'remote'}, 76: {'id': 76, 'name': 'keyboard'}, 77: {'id': 77, 'name': 'cell phone'}, 78: {'id': 78, 'name': 'microwave'}, 79: {'id': 79, 'name': 'oven'}, 80: {'id': 80, 'name': 'toaster'}, 81: {'id': 81, 'name': 'sink'}, 82: {'id': 82, 'name': 'refrigerator'}, 84: {'id': 84, 'name': 'book'}, 85: {'id': 85, 'name': 'clock'}, 86: {'id': 86, 'name': 'vase'}, 87: {'id': 87, 'name': 'scissors'}, 88: {'id': 88, 'name': 'teddy bear'}, 89: {'id': 89, 'name': 'hair drier'}, 90: {'id': 90, 'name': 'toothbrush'}}


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@獲取箱內物品':
        try:
            box_content = get_var()  #抓取ubidots資料
            re = ",".join(box_content)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=re))
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(get_var())))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='箱子裡面沒有東西！')) #若網路上沒有資料表示箱子裡面沒東西

# 將抓取到的數值陣列(id)換成名字並print出來   cmd為數字組成的字串(ex 0 18 45 3 ...)以空格分隔  
def get_box_content(cmd):
    cmd = cmd.strip()
    cmd_arr = cmd.split(" ") # 用空白分割
    cmd_arr_name = []
    for i in cmd_arr:
        cmd_arr_name.append(category[int(i)]['name']) ###
    return cmd_arr_name
        
#抓取ubidots資訊 
def get_var():
    #try:               
    #attempts = 0
    status_code = 400
    if status_code >= 400:            #sensor_value
        req = requests.get(url=URL, headers=HEADERS)
        status_code = req.status_code
    #get_box_content(int(float(req.text)))
    #get_box_content(req.text)
    return get_box_content(req.json()['last_value']['context']['id'])

if __name__ == '__main__':
    app.run()