from curses import keyname
from multiprocessing.spawn import old_main_modules
import speech_recognition as sr
import apa102
from gtts import gTTS
import os
import time
import re
import smtplib
import email.message
import RPi.GPIO as GPIO
#from catch import takePhoto
import catch1
import ubidots_send
import numpy as np

CONTROL_PIN = 17  # 11腳位，BCM編號為 17
PWM_FREQ = 50     # PWM 所使用的頻率
STEP=90           # 每次旋轉的角度
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ) # 宣告 pwm 控制物件
pwm.start(0) #開始 pwm 功能 
def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle
    #定義角度與工作週期的對應關係

global password #密碼在第一次使用之前為空
password = None
global emailAccount
emailAccount = None #讓使用者輸入
global key
key=0
global oldList
oldList = []
category_index = catch1.category_index
#第一次使用 : 先詢問密碼註冊，再讓使用者輸入email帳號
#之後一值偵測使用者由沒有說"開門"或"關門"
#若使用者說"修改密碼"就先讓使用者先講一次舊密碼，若正確就讓使用者修改密碼
#當門被關閉的時候寄信，"偵測到保險櫃被打開，內容物:....，...被拿出，...被放入"(開關門的資訊傳到雲端，再由乘程式抓下資訊並寄信)


#obtain audio from the microphone
r = sr.Recognizer()
'''
with sr.Microphone() as source:
    print("Please wait. Calibrating microphone...")
    #listen for 1 seconds and create the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=1)
    print("Say something!")
    audio=r.listen(source)
'''

def openKey():

    pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
    time.sleep(2)

def closeKey():

    pwm.ChangeDutyCycle(angle_to_duty_cycle(0))
    time.sleep(2)

def mail(emailAccount,msg_content):
    smtp=smtplib.SMTP('smtp.office365.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('s1081424@mail.yzu.edu.tw','123456789Sa')
    from_addr='s1081424@mail.yzu.edu.tw'
    to_addr=emailAccount

    #msg="Subject:Mail sent by Python scripts"
    msg=email.message.EmailMessage()
    msg["From"]=from_addr
    msg["To"]=to_addr
    msg["Subject"]="Warning"
    msg.add_alternative(msg_content)  #首次登入:"登入成功"，其他:箱內物品

    #status=smtp.sendmail(from_addr, to_addr, msg)
    status=smtp.send_message(msg)
    if status=={}:
        print("郵件傳送成功!")
    else:
        print("郵件傳送失敗!")
    smtp.quit()

def compare(newList):
    global oldList
    #print("newList:",newList)
    #print("oldList:",oldList)
    if len(list(set(newList).difference(oldList)))!=0 or len(list(set(oldList).difference(newList)))!=0: #若有東西被放入
        ss = []
        ss2 = []
        for i in oldList:
            ss.append(category_index[i]['name'])
        for i in newList:
            ss2.append(category_index[i]['name'])
        mail_mes = "Warning! 偵測到物品更動!\n"
        mail_mes += "原物品:"+",".join(ss)+"\n"
        mail_mes += "現在物品:"+",".join(ss2)+"\n"
        mail(emailAccount,mail_mes)
        oldList.clear()
        for i in newList:  # newList取代oldList
            oldList.append(i)

def instruction_listen(comm,source):  #處理開門指令
    global password
    if comm ==  "開門":
        #tts = gTTS(text='門已開啟', lang='zh-TW')
        #tts.save('door_open.mp3')
        #os.system('omxplayer -o local -p door_open.mp3 > /dev/null 2>&1')
        log_in(source)
    if comm ==  "關門":
        closeKey()
        tts = gTTS(text='門已關閉，主人請放心', lang='zh-TW')
        tts.save('door_close.mp3')
        os.system('omxplayer -o local -p door_close.mp3 > /dev/null 2>&1')
        catch1.takePhoto() #照相
        #print("id_list:",catch1.new_id_list) #輸出畫面物品id
        """if catch1.old_id_list!=None:
            print("old_id_list: ",catch1.old_id_list)"""
        ##########    
        ubidots_send.upload_ID(catch1.new_id_list)
        compare(catch1.new_id_list) 

    elif comm ==  "修改密碼": #考慮改成時間到就自動關門
        tts = gTTS(text='請說出舊密碼', lang='zh-TW')
        tts.save('said_old_psw.mp3')
        os.system('omxplayer -o local -p said_old_psw.mp3 > /dev/null 2>&1')
        
        audio = r.record(source,duration=10)
        old_psw = r.recognize_google(audio, language='zh-TW')
        old_psw = re.sub("請說出舊密碼","",old_psw)
        print("舊密碼:",old_psw)
        if old_psw != password:
            tts = gTTS(text='密碼錯誤，若要重新登入請再說一次修改密碼', lang='zh-TW')
            tts.save('login_error.mp3')
            os.system('omxplayer -o local -p login_error.mp3 > /dev/null 2>&1')
        else:
            tts = gTTS(text='請說出新的密碼', lang='zh-TW')
            tts.save('said_new_psw.mp3')
            os.system('omxplayer -o local -p said_new_psw.mp3 > /dev/null 2>&1')
            audio = r.record(source,duration=10) #聽使用者說的話
            password = r.recognize_google(audio, language='zh-TW') #紀錄剛剛聽到的話(中文)
            password=re.sub("請說出新的立馬","",password)
            password=re.sub("請說出新的密碼","",password)
            password=re.sub("請說出新的力嗎","",password)
            print('你的新密碼:',password)
            tts = gTTS(text='新密碼已修改', lang='zh-TW')
            tts.save('modified_new_psw.mp3')
            os.system('omxplayer -o local -p modified_new_psw.mp3 > /dev/null 2>&1')
            
        
def log_in(source):
    #若是第一次登入，先登記密碼再填寫email account
    global password
    if password == None:

        tts = gTTS(text='首次使用，請說出密碼', lang='zh-TW')
        tts.save('ask_psw.mp3')
        os.system('omxplayer -o local -p ask_psw.mp3 > /dev/null 2>&1')
        #audio1 = r.listen(source)
        #p=r.recognize_google(audio1, language='zh-TW')
        #time.sleep(10)
        audio = r.record(source,duration=10) #聽使用者說的話
        password = r.recognize_google(audio, language='zh-TW') #紀錄剛剛聽到的話(中文)
        password=re.sub("首次使用請說出密碼","",password)
        print('你的密碼:',password) 
        
        tts = gTTS(text='請在畫面輸入email帳號', lang='zh-TW')
        tts.save('ask_email.mp3')
        os.system('omxplayer -o local -p ask_email.mp3 > /dev/null 2>&1')
        global emailAccount
        emailAccount = input('Email:')
        mail(emailAccount,"登入成功")
    else: #登入
        tts = gTTS(text='請說密碼', lang='zh-TW')
        tts.save('login_psw.mp3')
        os.system('omxplayer -o local -p login_psw.mp3 > /dev/null 2>&1')
        #time.sleep(10)
        audio = r.record(source,duration=8) #聽使用者說的話"
        buffer_password = r.recognize_google(audio, language='zh-TW')
        buffer_password=re.sub("請說密碼","",buffer_password)
        buffer_password=re.sub("聽說密碼","",buffer_password)
        print("密碼:",buffer_password)
        if buffer_password != password:
            tts = gTTS(text='密碼錯誤，若要重新登入請再說一次開門', lang='zh-TW')
            tts.save('login_error.mp3')
            os.system('omxplayer -o local -p login_error.mp3 > /dev/null 2>&1')
        else: #登入成功
            openKey()
            
            tts = gTTS(text='登入成功，門已開啟', lang='zh-TW')
            tts.save('door_open.mp3')
            os.system('omxplayer -o local -p door_open.mp3 > /dev/null 2>&1')
           

# recognize speech using Google Speech Recognition
try:
    while True:
        with sr.Microphone() as source:
            #print("Please wait. Calibrating microphone...")
            #listen for 1 seconds and create the ambient noise energy level
            r.adjust_for_ambient_noise(source, duration=1)            
            print("說指令!(開門/修改密碼/關門)")
            #time.sleep(10)
            audio=r.record(source,duration=8) #聽使用者說的話
            """if audio==None:
                print("No")"""
            #print(type(audio))
            print("指令:",end="")

            print(r.recognize_google(audio, language='zh-TW')) #紀錄剛剛聽到的話(中文)
            instruction_listen(r.recognize_google(audio, language='zh-TW'),source) #處理"開門指令"
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")

except sr.RequestError as e:
    print("No response from Google Speech Recognition service: {0}".format(e))
#finally:
#    print("End")
    #leds.cleanup()