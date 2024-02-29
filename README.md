# 智慧儲物箱

- 使用樹梅派、影像辨識、智慧音箱、伺服馬達開發的智慧儲物箱，讓使用者身處何處都能取得箱中物品資訊。
- 提供了物品項變動警示，及箱子鎖定登入系統。

## :small_blue_diamond:System design and implementation

:small_orange_diamond:**Development tools:** Python, OpenCV, LINE bot, Heroku, Ubidots, 樹梅派, 智慧音箱, 伺服馬達

> 程式開始執行後，將由使用者選擇說出「開門」、「關門」、「修改密碼」，若使用者一開始說「開門」，則會要求使用者說出密碼，去設定開關密碼，並輸入電子郵件，當成功綁定電子郵件後，會寄發出第一封電子郵件（Figure 2）
![](https://github.com/jaifenny/Voice_controlled_smart_storage_box/blob/main/picture/1.jpg)


> 接著就能夠使用開門、關門和修改密碼的功能了，綁定電子郵件後，當說開門時會要求使用者說出密碼，若密碼與之前設定的密碼不吻合，則不會開門，相反若密碼吻合，伺服馬達會轉到 90 度（Figure 3），如果選擇更改密碼，則會要求使用者重新說出一次舊密碼，若舊密碼與之前的密碼不相符，程式會要求使用者再重新說出修改密碼，並重新驗證一次，若舊密碼與之前的密碼吻合則可以繼續說出新密碼，如果選擇關門，伺服馬達會轉到 0 度（Figure 4）
![](https://github.com/jaifenny/Voice_controlled_smart_storage_box/blob/main/picture/1.png)


> Webcam 會拍照並利用 opencv 進行物品辨識，再將紙箱內的物品上傳至 Ubidots，若上次關門的物品和現在紙箱內現有物品不一樣，則會傳送警告資訊和物品比對至電子郵件中（Figure5）
![](https://github.com/jaifenny/Voice_controlled_smart_storage_box/blob/main/picture/2.jpg)

> 加入LINE bot 保險箱監控（Figure 6）還可以即時查詢箱內的物品（Figure 7）
![](https://github.com/jaifenny/Voice_controlled_smart_storage_box/blob/main/picture/2.png)

![](https://github.com/jaifenny/Voice_controlled_smart_storage_box/blob/main/picture/3.png)

![](https://github.com/jaifenny/Voice_controlled_smart_storage_box/blob/main/picture/4.png)

## :small_blue_diamond: References
- 伺服馬達：https://is.gd/kFepSm
- LINE bot：https://github.com/yaoandy107/line-bot-tutorial

