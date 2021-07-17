import time
from PIL import ImageGrab
from PIL import Image,ImageFilter
import io 
import tkinter as tk
import os
import subprocess

def get_p(beilv = 1): #屏幕放大倍率
    root = tk.Tk()
    wei = root.winfo_screenwidth()
    hig = root.winfo_screenheight()
    root.destroy()
    return(int(wei*beilv), int(hig*beilv))

def screenshot(radius = 2):
    mypx = get_p(1.25) #屏幕放大倍率,我的电脑是125%
    img = ImageGrab.grab(bbox=(0, 0, mypx[0], mypx[1]))
    img = img.filter(ImageFilter.GaussianBlur(radius = radius))
    imgbyte = io.BytesIO()
    img.save(imgbyte, format='JPEG')
    return(imgbyte.getvalue())


#############下面为手机屏幕获取

def popen(com, is_out = False):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out = 'f'
    try:
        out = ex.stdout.read().decode("GBK")
    except:
        out = ex.stdout.read().decode("utf-8")
    return out

def get_screen_phone(radius = 2):
    res = os.popen("adb shell \"dumpsys window | grep mCurrentFocus\"")
    now_run = res.read()
    print(now_run, type(now_run))
    if(("com.tencent.mobileqq" in now_run) and radius != 0): #QQ在前台,模糊度增加
        radius += 3
    if(("com.tencent.mm" in now_run) and radius != 0): #微信在前台,模糊度增加
        radius += 3

    iname = str(int(time.time() * 1000))
    popen("adb shell /system/bin/screencap -p /sdcard/%s.png" % iname)
    popen("adb pull /sdcard/%s.png ./temp/%s.png" % (iname, iname))
    popen("adb shell rm /sdcard/%s.png" % iname)

    #try:
    img = Image.open("./temp/%s.png" % iname)
    img = img.convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(radius = radius))
    imgbyte = io.BytesIO()
    img.save(imgbyte, format='JPEG')
    os.remove("./temp/%s.png" % iname)
    return(imgbyte.getvalue())
    #except:
    #    return(screenshot(radius))




