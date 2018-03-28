# Today_Movbot
# Sebuah bot di telegram yang membantu anda untuk menemukan jadwal film yang tayang di theater Cinema XXI Kota Tangerang
# Bot ini tidak diendorse oleh Cinema XXI. Bot ini merupakan project pertama saya setelah mempelajari dasar-dasar pemrograman python
# dibuat menggunakan python 2.7

# import modul-modul yang dibutuhkan
import telebot
import urllib
import urllib2
import sys
import time
import os
from bs4 import BeautifulSoup
from flask import Flask, request


# initialize bot
bot = telebot.TeleBot(os.environ["BOT_TOKEN"])

server = Flask(__name__)

# daftar url
cinema21_url = {
    "tangcity": "http://www.21cineplex.com/theater/bioskop-tang-city-xxi,363,TGRTACI.htm",
    "balekota": "http://www.21cineplex.com/theater/bioskop-bale-kota-xxi,341,TGRBAKO.htm",
    "livingworld": "http://www.21cineplex.com/theater/bioskop-living-world-xxi,309,TGRLIWO.htm",
    "alamsutera": "http://www.21cineplex.com/theater/bioskop-alam-sutera-xxi,327,TGRALSU.htm",
    "supermallkarawacixxi": "http://www.21cineplex.com/theater/bioskop-supermal-karawaci-xxi,122,TGRKARA.htm",
    "smsserpong": "http://www.21cineplex.com/theater/bioskop-summarecon-mal-serpong-xxi,256,TGRSERO.htm",
    "aeon": "http://www.21cineplex.com/theater/bioskop-aeon-mall-bsd-city-xxi,378,TGRAEBS.htm",
    "cbdciledug": "http://www.21cineplex.com/theater/bioskop-cbd-ciledug-xxi,291,TGRCBCI.htm",
    "bintaroxchange": "http://www.21cineplex.com/theater/bioskop-bintaro-xchange-xxi,350,TGRBIXC.htm",
    "bintaromall": "http://www.21cineplex.com/theater/bioskop-bintaro-xxi,54,TGRBINT.htm",
    "bsdxxi": "http://www.21cineplex.com/theater/bioskop-bsd-xxi,126,TGRSERP.htm",
    "lottebintaro": "http://www.21cineplex.com/theater/bioskop-lotte-bintaro-xxi,328,TGRLOBI.htm",
    "supermallkarawaci": "http://www.21cineplex.com/theater/bioskop-supermal-karawaci,294,TGRLIKA.htm",
    "smsimax": "http://www.21cineplex.com/theater/bioskop-summarecon-mal-serpong-imax,355,TGRIXSS.htm",
    "aeonpremiere": "http://www.21cineplex.com/theater/bioskop-aeon-mall-bsd-city-premiere,379,TGRPRAB.htm",
    "alamsuterapremiere": "http://www.21cineplex.com/theater/bioskop-alam-sutera-premiere,330,TGRPRAS.htm",
    "livingworldpremiere": "http://www.21cineplex.com/theater/bioskop-living-world-premiere,310,TGRPRLW.htm",
    "smspremiere": "http://www.21cineplex.com/theater/bioskop-summarecon-mal-serpong-premiere,364,TGRPRSS.htm",
    "karawacipremiere": "http://www.21cineplex.com/theater/bioskop-supermal-karawaci-premiere,295,TGRPRKA.htm",
}


def user_url(msg, url_dict):
    formatted = msg.lower().replace(" ", "")
    if formatted in url_dict:
        url = url_dict[formatted]
    else:
        url = ''
        sys.exit()

    return url

def download_url (msg):

    url = user_url(msg, cinema21_url)
    headers = {"Users-Agent": "Mozilla/5.0 (Linux; Intel Linux 10_9_5)\
               AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
               "Accept": "text/html,application/xhtml+xml,application/xml;\
                        q=0.9,image/webp,*/*;q=0.8"}
    request = urllib2.Request(url, headers=headers)
    # membuka url
    try:
        page = BeautifulSoup(urllib2.urlopen(request), "html.parser")
    except urllib2.URLError as e:
        error_message = "Error %s HTTP." % e.reason
        sys.exit(error_message)

    return page

def normal_showtime(msg,chat_id):

    page = download_url(msg)

    # Theater info
    data = page.find("div", {"class": "col-m_462"}).findAll("div")
    theater = data[0].get_text()
    info = data[1].get_text()

    bot.send_message(chat_id, theater)
    bot.send_message(chat_id, info)

    html = page.find("div", {"id": "makan"}).findAll("tr", {"class": ["light", "dark"]})

    for elem in html:
        # Retrieve film thumbnails
        a = elem.find_all('a')
        img = a[0].find('img').get('src')
        urlpic = img.replace('50x60', '300x430')
        urllib.urlretrieve(urlpic, "1.jpg")
        file = open('1.jpg', 'rb')

        # Retrieve film titles
        a = elem.find_all('a')
        title = a[1].get_text()

        # Retrieve film schedules
        div = elem.find_all('div')
        td = elem.find_all('td')

        if div:
            schedule = div[0].get_text()
        else:
            schedule = td[1].get_text()

        film = title + '\n' + schedule

        bot.send_photo(chat_id, file)
        bot.send_message(chat_id, film)
        time.sleep(2)

def sundaynight_showtime(msg,chat_id):

    page = download_url(msg)

    html = page.find("div", {"id": "makan"}).find_next_sibling("div", {"id": "makan"}).findAll("tr", {"class": ["light", "dark"]})

    if html:
        for elem in html:
            # Retrieve film thumbnails
            a = elem.find_all('a')
            img = a[0].find('img').get('src')
            urlpic = img.replace('50x60', '300x430')
            urllib.urlretrieve(urlpic, "1.jpg")
            file = open('1.jpg', 'rb')

            # Retrieve film titles
            a = elem.find_all('a')
            title = a[1].get_text()

            # Retrieve film schedules
            div = elem.find_all('div')
            td = elem.find_all('td')

            if div:
                schedule = div[0].get_text()
            else:
                schedule = td[1].get_text()

            film = title + '\n' + schedule

            bot.send_photo(chat_id, file)
            bot.send_message(chat_id, film)
            time.sleep(2)
    else:
        bot.send_message(chat_id, "Tidak ada jadwal tayang lewat dari pukul 22.00")


# Handler
@bot.message_handler(commands=['start'])
@bot.message_handler(commands=['help'])
def welcome_message(message):
    msg = 'Jadwal film theater XXI di Kota Tangerang, ketik "/" dan pilih theater yang anda inginkan.'
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['tangcity', 'balekota', 'livingworld', 'alamsutera', 'supermallkarawacixxi', 'smsserpong', 'aeon',
                    'cbdciledug', 'bintaroxchange', 'bintaromall', 'bsdxxi', 'lottebintaro', 'supermallkarawaci', 'smsimax',
                    'aeonpremiere', 'alamsuterapremiere', 'livingworldpremiere', 'smspremiere', 'karawacipremiere'])
def show_film(message):
    chat_id = message.chat.id
    msg = message.text.lower()

    theater_list = ['/tangcity', '/balekota', '/livingworld', '/alamsutera', '/supermallkarawacixxi', '/smsserpong', '/aeon',
                    '/cbdciledug', '/bintaroxchange', '/bintaromall', '/bsdxxi', '/lottebintaro', '/supermallkarawaci',
                    '/smsimax', '/aeonpremiere', '/alamsuterapremiere', '/livingworldpremiere', '/smspremiere', '/karawacipremiere']

    day = time.strftime('a', time.gmtime())

    if msg in theater_list:
        theater = msg.replace('/', '')
        normal_showtime(theater,chat_id)
        # Cek, apakah hari ini sabtu atau minggu, bila benar maka menampilkan jadwal tayang yang lewat dari pukul 22.00
        if day == 'sat':
            sundaynight_showtime(theater,chat_id)
    else:
        bot.send_message(message.chat.id, 'Theater yang anda cari tidak ditemukan, harap ketik nama theater '
                                          'yang anda cari dengan benar')
        sys.exit()

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://thawing-cove-33377.herokuapp.com/bot")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)
