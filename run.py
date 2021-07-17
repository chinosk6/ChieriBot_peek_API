from flask import Flask,send_file,request
from os import environ
from urllib import parse
import io, time, os
from threading import Thread
import screenshot
import sys, random
import getrecentaudio
from system_hotkey import SystemHotkey
import threading
from rwini import *

app = Flask(__name__)

#class sstat:
#    def __init__(self, ispublic):
#        self.ispublic = ispublic #true公开
#
#    def change_public(self):
#        if(self.ispublic):
#            self.ispublic = False
#        else:
#            self.ispublic = True
#
#    def get_is_public(self):
#        return(self.ispublic)

class sstat:
    def change_public():
        gstat = 读配置项("dev.ini", "basic", "ispublic", "1") #1公开,其它私密
        if(gstat == "1"):
            写配置项("dev.ini", "basic", "ispublic", "0")
        else:
            写配置项("dev.ini", "basic", "ispublic", "1")

    def get_is_public():
        gstat = 读配置项("dev.ini", "basic", "ispublic", "1")
        if(gstat == "1"):
            return(True)
        else:
            return(False)

    def change_device():
        gstat = 读配置项("dev.ini", "basic", "dev", "1") #1pc,2手机
        if(gstat == "1"):
            写配置项("dev.ini", "basic", "dev", "2")
        else:
            写配置项("dev.ini", "basic", "dev", "1")

    def get_device():
        gstat = 读配置项("dev.ini", "basic", "dev", "1")
        return(gstat)

mst = sstat

def on_key(this, hotkey, args):
    if("s" in hotkey):
        if(mst.get_is_public()):
            mst.change_public()
            print("已设置为私密")
        else:
            mst.change_public()
            print("已设置为公开")

    if("c" in hotkey):
        if(mst.get_device() == "1"):
            mst.change_device()
            print("已切换到手机")
        else:
            mst.change_device()
            print("已切换到电脑")

def async_qwq(f):
    def task_qwq(*args, **kwargs):
        t = Thread(target=f, args=args, kwargs=kwargs)
        t.start()
    return(task_qwq)

@async_qwq
def insertlog(r_ip, r_ua, r_id, r_ref, r_fullheader):
    connect_database.conn_mysql().insert_logs(r_ip = r_ip, r_ua = r_ua, r_id = r_id, r_ref = r_ref, r_fullheader = r_fullheader)

@async_qwq
def insertlog_sqlite(r_ip, r_ua, r_id, r_ref, r_fullheader):
    connect_database.conn_sqlite.insert_db(".\\conn_logs\\log.db","insert into log VALUES (?,?,?,?,?,?)", para=(shaa.timestamp_to_text(time.time()), r_ip, r_ua, r_id, r_ref, r_fullheader))

@app.route('/my/screen', methods=["GET"])
def req():

    r = request.args.get("r")
    k = request.args.get("k")
    if(r == None or r == '' ):
        r = 2.5
    else:
        r = float(r)
        if(r < 2):
            if(k != "mykeyowo"):
                return("喵噗噗,不能随便看哦~", 403)
    if(mst.get_is_public()):
        if(mst.get_device() == "1"): #1，返回电脑屏幕
            return(send_file(
                io.BytesIO(screenshot.screenshot(r)),
                #attachment_filename='arcsig by \'sunset',
                mimetype='image/jpg'
            ), 200)
        else:
            if(r != 0):
                r = r + 4
            return(send_file(
                io.BytesIO(screenshot.get_screen_phone(r)),
                #attachment_filename='arcsig by \'sunset',
                mimetype='image/jpg'
            ), 200)

    else:
        with open("secret.jpg", "rb") as fi:
            return(send_file(
                io.BytesIO(fi.read()),
                #attachment_filename='arcsig by \'sunset',
                mimetype='image/jpg'
            ), 200)

@app.route('/my/getaud', methods=["GET", "POST"])
def getaud():
    if(mst.get_is_public()):
        if(mst.get_device() == "1"): #设备为1时才输出音频
            return(send_file(
                getrecentaudio.get_aud(),
                #attachment_filename='arcsig by \'sunset',
                mimetype='audio/x-wav'
            ), 200)

    else:
        with open("不给.wav", "rb") as fi:
            return(send_file(
                io.BytesIO(fi.read()),
                #attachment_filename='arcsig by \'sunset',
                mimetype='audio/x-wav'
            ), 200)   

    return("ok", 200)

@app.route('/check', methods=["GET", "POST"])
def check():
    return("ok", 200)

def s():
    hk = SystemHotkey(consumer=on_key)
    hk.register(("alt", "s"), 1, 2, 3, 4) #切换公开/私密
    hk2 = SystemHotkey(consumer=on_key)
    hk2.register(("alt", "c"), 1, 2, 3, 4) #切换设备

if __name__ == '__main__':                        #正式部署请使用下面的代码
    s()
    app.run("127.0.0.1", 1919, debug=True) 
#if __name__ == "__main__":
#    s()
#    from waitress import serve
#    serve(app, host = "127.0.0.1", port = 1919)
