from flask import Flask, send_file, request
import io
from threading import Thread
import screenshot
import getrecentaudio
from system_hotkey import SystemHotkey
from to_system_tray import sstat, start_tray

app = Flask(__name__)

mst = sstat


def on_key(this, hotkey, args):
    if ("s" in hotkey):
        mst.change_public()

    if ("c" in hotkey):
        mst.change_device()


def async_qwq(f):
    def task_qwq(*args, **kwargs):
        t = Thread(target=f, args=args, kwargs=kwargs)
        t.start()

    return (task_qwq)


@app.route('/my/screen', methods=["GET"])
def req():
    r = request.args.get("r")
    k = request.args.get("k")
    if (r == None or r == ''):
        r = 3
    else:
        r = float(r)
        if (r < 2):
            if (k != "mykeyowo"):
                return ("喵噗噗,不能随便看哦~", 403)
    if (mst.get_is_public()):
        if (mst.get_device() == "1"):  # 1，返回电脑屏幕
            return (send_file(
                io.BytesIO(screenshot.screenshot(r)),
                # attachment_filename='arcsig by \'sunset',
                mimetype='image/jpg'
            ), 200)
        else:
            if (r != 0):
                r = r + 4
            return (send_file(
                io.BytesIO(screenshot.get_screen_phone(r)),
                # attachment_filename='arcsig by \'sunset',
                mimetype='image/jpg'
            ), 200)

    else:
        with open("secret.jpg", "rb") as fi:
            return (send_file(
                io.BytesIO(fi.read()),
                # attachment_filename='arcsig by \'sunset',
                mimetype='image/jpg'
            ), 200)


@app.route('/my/getaud', methods=["GET", "POST"])
def getaud():
    if (mst.get_is_public()):
        if (mst.get_device() == "1"):  # 设备为1时才输出音频
            return (send_file(
                getrecentaudio.get_aud(),
                # attachment_filename='arcsig by \'sunset',
                mimetype='audio/x-wav'
            ), 200)

    else:
        with open("不给.wav", "rb") as fi:
            return (send_file(
                io.BytesIO(fi.read()),
                # attachment_filename='arcsig by \'sunset',
                mimetype='audio/x-wav'
            ), 200)

    return ("ok", 200)


@app.route('/check', methods=["GET", "POST"])
def check():
    if mst.get_device() != "1":  # 手机接入时无声音
        return ("noaud", 200)
    return ("ok", 200)


def s():
    hk = SystemHotkey(consumer=on_key)
    hk.register(("alt", "s"), 1, 2, 3, 4)  # 切换公开/私密
    hk2 = SystemHotkey(consumer=on_key)
    hk2.register(("alt", "c"), 1, 2, 3, 4)  # 切换设备


if __name__ == '__main__':
    s()
    start_tray()
    app.run("0.0.0.0", 1919, debug=False)
