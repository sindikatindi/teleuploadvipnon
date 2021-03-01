#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.


# ██╗░░██╗░█████╗░██╗░░░██╗░█████╗░  ███╗░░░███╗░█████╗░██╗░░░██╗
# ██║░░██║██╔══██╗╚██╗░██╔╝██╔══██╗  ████╗░████║██╔══██╗██║░░░██║
# ███████║███████║░╚████╔╝░██║░░██║  ██╔████╔██║███████║██║░░░██║
# ██╔══██║██╔══██║░░╚██╔╝░░██║░░██║  ██║╚██╔╝██║██╔══██║██║░░░██║
# ██║░░██║██║░░██║░░░██║░░░╚█████╔╝  ██║░╚═╝░██║██║░░██║╚██████╔╝
# ╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░  ╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚═════╝░

# ███╗░░██╗░██████╗░░█████╗░██████╗░░█████╗░██╗███╗░░██╗░█████╗░
# ████╗░██║██╔════╝░██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔══██╗
# ██╔██╗██║██║░░██╗░███████║██████╔╝███████║██║██╔██╗██║╚═╝███╔╝
# ██║╚████║██║░░╚██╗██╔══██║██╔═══╝░██╔══██║██║██║╚████║░░░╚══╝░
# ██║░╚███║╚██████╔╝██║░░██║██║░░░░░██║░░██║██║██║░╚███║░░░██╗░░
# ╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░░░╚═╝░░


# ░░█ ▄▀█ █▄░█ █▀▀ ▄▀█ █▄░█   █▄░█ ▄▀█ █▄▀ ▄▀█ █░░   █▄█ ▄▀█ █░█   ▀ ▀▄
# █▄█ █▀█ █░▀█ █▄█ █▀█ █░▀█   █░▀█ █▀█ █░█ █▀█ █▄▄   ░█░ █▀█ █▀█   ▄ ▄▀


# █▀▀ █▀█ █▀▀ █▀▄ █ ▀█▀   ▀
# █▄▄ █▀▄ ██▄ █▄▀ █ ░█░   ▄

# █░█ ▀█▀ ▀█▀ █▀█ █▀ ▀ ░░▄▀ ░░▄▀ ▀█▀ ░ █▀▄▀█ █▀▀ ░░▄▀ █▀▄▀█ ▄▀█ █▄░█ █▀▀ █▀█ █░░ █ █░█ █▀▀ █▀▄ █▀█ █░█░█ █▄░█ █░░ █▀█ ▄▀█ █▀▄
# █▀█ ░█░ ░█░ █▀▀ ▄█ ▄ ▄▀░░ ▄▀░░ ░█░ ▄ █░▀░█ ██▄ ▄▀░░ █░▀░█ █▀█ █░▀█ █▄█ █▄█ █▄▄ █ ▀▄▀ ██▄ █▄▀ █▄█ ▀▄▀▄▀ █░▀█ █▄▄ █▄█ █▀█ █▄▀
# 

from __future__ import print_function
from __future__ import unicode_literals
import logging
import youtube_dl
import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram_upload.client import Client
import telegram
import requests
import urllib.request
import youtube_dl.utils
import json
import os.path
from datetime import datetime
from pytz import timezone
import time
import re
import math 
from telethon import TelegramClient
from functools import partial
from telegram_upload.exceptions import ThumbError, TelegramUploadDataLoss, TelegramUploadNoSpaceError
from telegram_upload.files import get_file_attributes, get_file_thumb
from telethon.version import __version__ as telethon_version
from telethon.tl.types import Message, DocumentAttributeFilename
from telethon.utils import pack_bot_file_id
import psycopg2


# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


akunUser = Config.AUTH_USERS


api_id = Config.APP_ID
api_hash = Config.API_HASH
bot_token = Config.TG_BOT_TOKEN

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
bot = telegram.Bot(token=bot_token)
        
def mangolive(link):
    fmt = "[%H:%M-%m/%d/%y]"
    timezonelist = 'Asia/Jakarta'
    now_time = datetime.now(timezone(timezonelist))
    waktu = now_time.strftime(fmt)
    content = link.strip().split("_")
    API_ENDPOINT = "http://api.yogurtlive.me/user/get"
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json", 
    }
    data = {
      "build": 141,
      "channel": "offical",
      "imei": "647215788421291",
      "device": "ASUS_Z01Q(7.1.2)",
      "params": {
        "tid": content[1]
      },
      "platform": "Android",
      "subChannel": "",
      "version": "1.4.1"
    }
    try:
        r = requests.post(url = API_ENDPOINT, data=json.dumps(data),headers=headers, timeout=5)
        data_live = r.json()
        nama = data_live['data']['user']['name']
        shortId = data_live['data']['user']['shortId']
        with open("namahost.txt", "w", encoding="utf-8") as f:
            f.write(str(nama)+' - '+str(shortId)+' - Mangolive - '+str(waktu))
        return str(nama)+' - '+str(shortId)+' - Mangolive - '+str(waktu)
    except:
        with open("namahost.txt", "w", encoding="utf-8") as f:
            f.write(str(content[1])+' - Mangolive - '+str(waktu))
        return str(content[1])+' - Mangolive - '+str(waktu)

def ambilnama(idx):
    connection = psycopg2.connect(user="bzukhuhoiqaksy",
                                    password="a8c8025cd6a25b081b629f00d6714ac8d4b2c211a423db2ff2bac6adc818855d",
                                    host="ec2-3-214-3-162.compute-1.amazonaws.com",
                                    port="5432",
                                    database="drtesg2ah18ti")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM host WHERE idx = %s",[idx])
    connection.commit()
    tupples = cursor.fetchone()
    return tupples

def sugarlive(link):
    fmt = "[%H:%M-%m/%d/%y]"
    timezonelist = 'Asia/Jakarta'
    now_time = datetime.now(timezone(timezonelist))
    waktu = now_time.strftime(fmt)
    content = link.strip().split("_")
    namahost = ambilnama(content[1])
    if namahost is not None:
        with open("namahost.txt", "w", encoding="utf-8") as f:
            f.write(str(namahost[2])+' - '+str(namahost[1])+' - Sugarlive - '+str(waktu))
        return str(namahost[2])+' - '+str(namahost[1])+' - Sugarlive - '+str(waktu)
    else:
        with open("namahost.txt", "w", encoding="utf-8") as f:
            f.write(str(content[1])+' - Sugarlive - '+str(waktu))
        return str(content[1])+' - Sugarlive - '+str(waktu)

def upload(update: Update, context: CallbackContext) -> None:
    # print(update)
    with open('namahost.txt') as f:
        content = f.readlines()
    print(content[0])

    if os.path.isfile('@mangolivedownload.mp4'):
        print ("File exist")
        os.remove('@mangolivedownload.mp4')
        
    if os.path.isfile('@mangolivedownload.flv'):
        print ("File exist")
        update.message.reply_text('File Masih ada dan akan di upload ulang :)')
        convertText = update.message.reply_text('Sedang menconvert video')
        subprocess.call(['ffmpeg', '-i', '@mangolivedownload.flv', '-codec', 'copy', '@mangolivedownload.mp4','-y'])
        try:
            bot.deleteMessage(message_id =convertText['message_id'], chat_id =convertText['chat']['id']) 
        except:
            pass
        niceclient('@mangolivedownload.mp4',content[0], update, context)

    elif os.path.isfile('@mangolivedownload.flv.part'):
        print ("File exist")
        update.message.reply_text('File Masih ada dan akan di upload ulang :)')
        os.rename('@mangolivedownload.flv.part','@mangolivedownload.flv')
        convertText = update.message.reply_text('Sedang menconvert video')
        subprocess.call(['ffmpeg', '-i', '@mangolivedownload.flv', '-codec', 'copy', '@mangolivedownload.mp4','-y'])
        try:
            bot.deleteMessage(message_id =convertText['message_id'], chat_id =convertText['chat']['id']) 
        except:
            pass
        niceclient('@mangolivedownload.mp4',content[0], update, context)

    else:
        update.message.reply_text('File sudah terhapus, server merestart ulang :(')
    

def start(update: Update, context: CallbackContext) -> None:
    # print(update)
    update.message.reply_text('Bot Sudah Siap Download! Kirim Link Sekarang :)')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

def echo(update: Update, context: CallbackContext) -> None:
    if os.path.isfile('@mangolivedownload.mp4'):
        print ("File exist")
        os.remove('@mangolivedownload.mp4')

    if os.path.isfile('@mangolivedownload.mp4.part'):
        print ("File exist")
        os.remove('@mangolivedownload.mp4.part')

    if os.path.isfile('@mangolivedownload.flv'):
        print ("File exist")
        os.remove('@mangolivedownload.flv')
        
    if os.path.isfile('@mangolivedownload.flv.part'):
        print ("File exist")
        os.remove('@mangolivedownload.flv.part')
        
    youtube_dl.utils.std_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    start = time.time()
    findText=re.findall(r'(?<=yogurtlive)', update.message.text)
    findTextt=re.findall(r'(?<=sugarlive)', update.message.text) 
    findTexttt=re.findall(r'(?<=flv)', update.message.text) 

    if findText:
        namaFile = mangolive(update.message.text)
        url=update.message.text
        url=url.replace('.flv','')
        print(namaFile)
        print('Download Dari Mangolive')
    elif findTextt:
        namaFile = sugarlive(update.message.text)
        url=update.message.text
        url=url.replace('.flv','')
        print(namaFile)
        print('Download Dari Sugarlive')
    else:
        url=update.message.text
        namaFile = '@mangolivedownload'

    uploadText = update.message.reply_text('Sedang Di Download '+str(namaFile))

    if findText or findTextt or findTexttt:
        outtmpl = '@mangolivedownload.flv'
        dbl = partial(my_hook,start=start,uploadText= uploadText,namaFile=str(namaFile))
    else:
        outtmpl = '@mangolivedownload.mp4'
        dbl = partial(progress_for_pyrogram,total='',ud_type='Sedang Download',start=start,uploadText= uploadText,namaFile=str(namaFile))

    ydl_opts = {
        'outtmpl': outtmpl,
        'format': 'best',
        'logger': MyLogger(),
        'progress_hooks': [dbl],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        convertText = update.message.reply_text('Sedang menconvert video')
        subprocess.call(['ffmpeg', '-i', outtmpl, '-codec', 'copy', '@mangolivedownload.mp4','-y'])
        try:
            bot.deleteMessage(message_id =convertText['message_id'], chat_id =convertText['chat']['id']) 
        except:
            pass
        niceclient('@mangolivedownload.mp4',namaFile, update, context)

    except:
        try:
            url = update.message.text
            video_name = url.split('/')[-1]
            print ("Downloading file:%s" % video_name)
            urllib.request.urlretrieve(url, '@mangolivedownload.mp4') 
            print ("Downloading :%s Selesai" % video_name)
            print(os.path.getsize('@mangolivedownload.mp4'))
            niceclient('@mangolivedownload.mp4','@mangolivedownload',update,context)
        except:
            update.message.reply_text('Link Mati/Bot Tidak Support')
    
class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def my_hook(d,start,uploadText,namaFile):
    message_id=uploadText['message_id']
    chat_id=uploadText['chat']['id']

    if d['status'] == 'finished':
        print('Download RTMP SELESAI')
        # file_tuple = os.path.split(os.path.abspath(d['filename']))
        # print("Done downloading {}".format(d['filename']))
        try:
            bot.deleteMessage(message_id =message_id, chat_id =chat_id) 
        except:
            pass

    if d['status'] == 'downloading':
        print(d['filename'], d['_speed_str'], d['_percent_str'], d['_eta_str'])
        now = time.time()
        diff = now - start
        if round(diff % 10.00) == 0:
            elapsed_time = round(diff) * 1000
            elapsed_time = TimeFormatter(milliseconds=elapsed_time)
            progress = "[█████████████░░░]"
            tmp = progress + "\nSpeed: {0}/s\nElapsed time: {1}\n".format(d['_speed_str'],elapsed_time)
            print("{0} {1}\n {2}".format("Sedang Download",namaFile,tmp))
            try:
                bot.editMessageText(message_id =message_id, chat_id =chat_id,
                    text="{0} {1}\n {2}".format("Sedang Download",namaFile,tmp)
                )
            except:
                pass

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def progress_for_pyrogram(current,total,ud_type,start,uploadText,namaFile):
    # message_id= message['message_id']
    # chat_id= message['chat']['id']
    if ud_type == 'Sedang Download':
       total=current['total_bytes']
       current=current['downloaded_bytes']
    else:
        current = current
        total = total
    print(ud_type , current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))
    message_id=uploadText['message_id']
    chat_id=uploadText['chat']['id']
    
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nElapsed time : {3}\nETA: {4}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        # print("{}\n {}".format(
        #           ud_type,
        #           tmp
        #       ))
        try:
            bot.editMessageText(message_id =message_id, chat_id =chat_id,
                text="{} {}\n {}".format(
                    ud_type,
                    namaFile,
                    tmp
                )
            )

        except:
            pass

    if current == total:
        try:
            bot.deleteMessage(message_id =message_id, chat_id =chat_id)
        except:
            pass


def upload_video(uploadText,name,namaFile):
    print('sedang upload ' +str(namaFile))
    start = time.time()
    filename = name
    dbl = partial(progress_for_pyrogram,ud_type='Sedang Upload',start=start,uploadText= uploadText,namaFile=namaFile)

    async def upload_file():
        file = await client.upload_file(filename, progress_callback=dbl)
        file_name = os.path.basename(filename)
        file_size = os.path.getsize(filename)
        thumb = None
        try:
            thumb = get_file_thumb(filename)
        except ThumbError as e:
            print('{}'.format(e), err=True)
        try:
            attributes = get_file_attributes(filename)
            try:
                await client.send_file(akunUser, file, thumb=thumb, caption=namaFile, attributes=attributes, supports_streaming=True)
                print('berhasil')
                # bot.send_message('-445921165', 'update.message.text' )

            finally:
                print('Upload Video berhasil')
        finally:
            if thumb:
                os.remove(thumb)
        print(file)

    with client:
        client.loop.run_until_complete(upload_file())

def niceclient(name, namaFile, update: Update, context: CallbackContext):
    print(name)
    try:
        ya = os.path.getsize(name)
        print(ya)
        try:    
            if ya > 1900000000:
                halo = subprocess.check_output(['python', 'ffmpegsplit.py' , '-f', name, '-s', '3600'])
                halo = halo.decode("utf-8") 
                print('INI HASILNYA : '+str(halo))
                findText=re.findall(r'(?<=SPLIT COUNT =)(.*?)(?= BUAH)', halo)
                print(findText[0])
                rep = name.replace('.mp4','')
                update.message.reply_text('Video size sebesar : '+str(round(ya/1000000))+' MB akan di split menjadi ' +str(findText[0]) +' Video')
                for x in range(int(findText[0])):
                    sizesplit = os.path.getsize(rep+'-'+str(x+1)+'-of-'+str(findText[0])+'.mp4')

                    print('Sedang Upload Video ke '+str(x+1))
                    print('Sedang Upload Sebesar '+ str(round(sizesplit/1000000))+' MB')
                    print(rep+'-'+str(x+1)+'-of-'+str(findText[0])+'.mp4')

                    uploadText = update.message.reply_text('Sedang Upload Video ke '+str(x+1)+ ' dari ' +str(findText[0])+' video, Sebesar '+ str(round(sizesplit/1000000))+' MB')
                    nameT = rep+'-'+str(x+1)+'-of-'+str(findText[0])+'.mp4'
                    upload_video(uploadText,nameT,namaFile)
                    time.sleep(2)
                    try:
                        os.remove(rep+'-'+str(x+1)+'-of-'+str(findText[0])+'.mp4')
                    except:
                        print('sudah di hapus')
                    print('berhasil upload')
                try:
                    os.remove(name)
                    os.remove('@mangolivedownload.flv')
                except:
                    print('sudah di hapus')
                update.message.reply_text('Semua Video Berhasil Di Upload, Bot Bisa Digunakan kembali. :)')

            else:
                print('Sedang Upload Sebesar '+ str(round(ya/1000000))+' MB')
                uploadText = update.message.reply_text('Sedang Upload Sebesar '+ str(round(ya/1000000))+' MB')
                upload_video(uploadText,name,namaFile)
                time.sleep(2)
                try:
                    os.remove(name)
                    os.remove('@mangolivedownload.flv')
                except:
                    print('sudah di hapus')
                print('berhasil upload')
                update.message.reply_text('Video Berhasil Di Upload, Bot Bisa Digunakan kembali. :)')

        except:
            update.message.reply_text('Upload Gagal :( , server tidak stabil. atau Link Mati/Salah')
    except:
        update.message.reply_text('Link Mati/Host Offline')

def main():
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("upload", upload))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
