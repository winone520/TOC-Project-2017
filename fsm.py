# -*- coding: utf-8 -*-
from transitions.extensions import GraphMachine
import requests
from bs4 import BeautifulSoup
from random import randint
import telegram

API_TOKEN = 'Your_API_Token'
bot = telegram.Bot(token=API_TOKEN)

taiwan=['臺北市','新北市','桃園市','臺中市','臺南市','高雄市','基隆市','新竹縣','新竹市','苗栗縣','彰化縣','南投縣','雲林縣','嘉義縣','嘉義市','屏東縣','宜蘭縣','花蓮縣','臺東縣','澎湖縣','金門縣','連江縣']
weather_url='http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey=CWB-704B646E-753E-4DB3-A41E-3CD4149DAF04'
rand_reply=['你以為我會跟你聊天嗎?下去!','指令是不是打錯了呢?','你再亂打信不信我打爆你?','E...T...go home','try this => /help','img/black_question.jpg']
chat_room_id=[]


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
    def on_enter_user(self, update):
        custom_keyboard = [['/map', '/calendar','/weather','/phone','/question'], ['/food','/links', '/download','/chat','/help']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat.id, text="歡迎繼續使用成大一把通喔~\n輸入 /help 來看本bot是怎麼使用的吧!", reply_markup=reply_markup)

    def is_starting(self, update):
        text = update.message.text
        if '/start' in text:
            return 1
        else:
            return 0

    def on_enter_startState(self, update):
        custom_keyboard = [['/map', '/calendar','/weather','/phone','/question'], ['food','/links', '/download','/chat','/help']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat.id,  text="歡迎來到 *成大資訊一把通* ！\n指令都在下面的鍵盤上了~", reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
        self.go_back(update)

    def someone_need_help(self, update):
        text = update.message.text
        if '/help' in text:
            return 1
        else:
            return 0

    def on_enter_help(self, update):
        bot.send_message(chat_id=update.message.chat.id,text="歡迎來到 *成大資訊一把通* ！\n想問 `成大校園地圖` 請輸入 /map\n想問 `成大行事曆` 請輸入 /calendar\n想問 `天氣` 請輸入 /weather\n想問 `成大相關電話` 請輸入 /phone\n想問 `學生常見Q&A` 請輸入 /question\n想問 `吃什麼` 請輸入 /food\n想問 `成大相關連結` 請輸入 /links\n想要 `下載學生相關文件(請假單...)` 請輸入 /download\n想要 `進入聊天室` 請輸入 /chat ", parse_mode=telegram.ParseMode.MARKDOWN)
        self.go_back(update)

    def NCKU_map(self, update):
        text = update.message.text
        if '/map' in text:
            return 1
        else:
            return 0

    def on_enter_map(self, update):
        update.message.reply_photo(open('img/map.jpg', 'rb'))
        self.go_back(update)

    def NCKU_calendar(self, update):
        text = update.message.text
        if '/calendar' in text:
            return 1
        else:
            return 0

    def on_enter_calendar(self, update):
        update.message.reply_document(open('img/calendar.pdf', 'rb'))
        self.go_back(update)

    def NCKU_download(self, update):
        text = update.message.text
        if '/download' in text:
            return 1
        else:
            return 0

    def on_enter_download(self, update):
        custom_keyboard = [['1','2','3','exit']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat.id,text='輸入 `1` 下載《成功大學學生請假單》\n輸入 `2` 下載《成功大學學生公假請假單》\n輸入 `3` 下載《成功大學資訊系補棄選申請表》\n輸入 `exit` 取消動作', parse_mode=telegram.ParseMode.MARKDOWN,reply_markup=reply_markup)
        return 1
    

    def NCKU_download_detail(self, update):
        text = update.message.text
        if text.isdigit():
            if  1 <= int(text) <= 3:
                return 1
        elif text != 'exit':
            update.message.reply_photo(open('img/black_question.jpg', 'rb')) 
            update.message.reply_text("你這樣不乖喔 罰你重來一遍")

            self.go_back(update)
        else:
            self.go_back(update)
        

    def on_enter_downloadDetail(self, update):
        text = update.message.text
        
        if text == '1':
            update.message.reply_document(open('img/成功大學學生請假單.odt', 'rb'))
        elif text == '2':
            update.message.reply_document(open('img/成功大學學生公假請假單.odt', 'rb'))            
        elif text == '3':
            update.message.reply_document(open('img/成功大學資訊系補棄選申請表.odt', 'rb'))
        self.go_back(update)

    def NCKU_phone(self, update):
        text = update.message.text
        if  '/phone' in text:
            return 1
        else:
            return 0
        
    def on_enter_phone(self, update):
        bot.send_message(chat_id=update.message.chat.id,text="`成功大學總機`：06-2757575\n`校安中心`：06-2757575,`分機`55555\n`駐警隊`：06-2757575,`分機`66666\n`護送天使`：06-2757575,`分機`50880\n`校安中心`：06-2381187", parse_mode=telegram.ParseMode.MARKDOWN)      
        self.go_back(update)

    def NCKU_link(self, update):
        text = update.message.text
        if  '/links' in text:
            return 1
        else:
            return 0
        
    def on_enter_links(self, update): 
        bot.send_message(chat_id=update.message.chat.id, text="[成大官網](http://web.ncku.edu.tw/bin/home.php)\n[成功入口](https://i.ncku.edu.tw/)\n[moodle](http://moodle.ncku.edu.tw)\n[圖書館專區](https://i.ncku.edu.tw/zh-hant/apps-list-service/652)\n[成績查詢](http://140.116.165.71:8888/ncku/qrys02.asp)\n[FB成大選課版](https://www.facebook.com/groups/637099219647956/)\n[FB成大二手交易版](https://www.facebook.com/groups/384397068383429/?ref=bookmarks)", parse_mode=telegram.ParseMode.MARKDOWN)
        self.go_back(update)

    def ask_weather(self, update):
        text = update.message.text
        if  '/weather' in text:
            return 1
        else:
            return 0
        
    def on_enter_weather(self, update):
        custom_keyboard = [['1','2','3','4','5','6'],['7','8','9','10','11','12'],['13','14','15','16','17','18'],['19','20','21','22','exit']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        reply = '輸入對應數字獲取當地天氣：\n'
        for i in range(0,22):
            reply = reply + ' `' + str(i+1) + '`' + '\t' + '《' + taiwan[i] + '》\n'
        bot.send_message(chat_id=update.message.chat.id,text=reply, parse_mode=telegram.ParseMode.MARKDOWN ,reply_markup=reply_markup)

        return 1

    def ask_weather_where(self, update):      
        text = update.message.text
        if text.isdigit():
            if  1 <= int(text) <= 22:
                update.message.reply_text("請稍等一下，我先卜個掛....")
                return 1
            else:
                update.message.reply_photo(open('img/black_question.jpg', 'rb')) 
                update.message.reply_text("你這樣不乖喔 罰你重來一遍")
                self.go_back(update)
        elif text != 'exit': 
            update.message.reply_photo(open('img/black_question.jpg', 'rb')) 
            update.message.reply_text("你這樣不乖喔 罰你重來一遍")
            self.go_back(update)
        else:
            self.go_back(update)
        

    def on_enter_weatherWhere(self, update):
        text = update.message.text
        website=requests.get(weather_url)
        soup = BeautifulSoup(website.text,"html.parser")
        str_pointer=soup.find(string=taiwan[int(text)-1]) #find where the tag is
        str_pointer=str_pointer.find_parents("location")
        reply='地點： '+taiwan[int(text)-1]+ '\n'
        for i in range(0,3):
            for fragment in str_pointer:
                start_time = fragment.findAll('starttime')[i].string[:16] 
                end_time = fragment.findAll('endtime')[i].string[:16] 
                weather =fragment.findAll('parametername')[i].string  #find the first weather
                reply = reply + start_time +'~' + end_time +' - '+ weather + '\n'

        update.message.reply_text(reply)
        self.go_back(update)


    def go_chatroom(self, update):
        text = update.message.text
        if  '/chat' in text:
            reply = "welcome " + update.message.chat.first_name + "!\n現在就可以開始聊天了!\n輸入 /exit 來離開聊天室"
            boardcast = update.message.chat.first_name + ' 加入了聊天室!'
            update.message.reply_text(reply)
            chat_room_id.append(update.message.chat.id)

            for member_id in chat_room_id:
                bot.send_message(chat_id=member_id,text=boardcast)

            return 1
        else:
            return 0
        
    def on_enter_chat(self, update):
        reply_markup = telegram.ReplyKeyboardHide()
        bot.send_message(chat_id=update.message.chat.id,text=reply ,reply_markup=reply_markup)
        return 1

    def is_typing(self, update):
        text = update.message.text
        if  '/exit' in text:
            leaveReply = update.message.chat.first_name + "離開聊天室"
            for member_id in chat_room_id:
                bot.send_message(chat_id=member_id,text=leaveReply)
            
            chat_room_id.remove(update.message.chat.it)
            self.go_back(update)
        else:
            return 1
        
    def on_enter_typingRoom(self, update): 
        fullReply =  update.message.chat.first_name + ": " + update.message.text
        for member_id in chat_room_id:
                bot.send_message(chat_id=member_id,text=fullReply)
        self.still_chating(update)

    def ask_question(self, update):
        text = update.message.text
        if  '/question' in text:
            return 1
        else:
            return 0
        
    def on_enter_question(self, update):
        reply = '`Q1. 如何申請在學證明？`\nA: 至註冊組投幣自動繳費機申請紙本在學證明 (20元/份)。\n\n`Q2. 學生證遺失如何申請補發?`\nA: \n1.  採[數位學生證線上掛失辦理](http://id.ncku.edu.tw/login.php)(註冊組首頁>學生線上服務)或親自註冊組1號櫃台辦理線上掛失程序\n2.   補發者至自動投幣機繳費NT$200元。憑收據至註冊組辦理補發(1號櫃台將撕取收執聯)\n\n`Q3. 如何辦理選課退選？`\nA: 依選課公告退選期間,至註冊組首頁>學生線上服務>選課系統點選 退選功能申請\n\n`Q4. 身分證掉了，該怎麼補辦身分證?`\nA:\n*應備證件*:\n1.本人印章(或簽名)。\n2.本人戶口名簿正本或貼有相片之身分證明文件。\n3.本人最近2年內拍攝之符合規格相片1張\n*規費*：每張收費新臺幣200元\n*受理戶政事務所*：任一戶政事務所申請'
        bot.send_message(chat_id=update.message.chat.id,text=reply, parse_mode=telegram.ParseMode.MARKDOWN )
        self.go_back(update)

    def ask_food(self, update):
        text = update.message.text
        if  '/food' in text:
            return 1
        else:
            return 0
        
    def on_enter_eat(self, update):
        reply = '......別問我 我也想知道今天要吃什麼'
        update.message.reply_text(reply)
        self.go_back(update)


    def use_fault_command(self, update):
        return 1
        
    def on_enter_faultCommand(self, update):
        num = randint(0,7)
        if num <= 4:
            update.message.reply_text(rand_reply[num])
        else:
            update.message.reply_photo(open(rand_reply[5], "rb"))
        self.go_back(update)