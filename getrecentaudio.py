import os, io
import pyaudio
import threading
import wave
import time
from datetime import datetime
import random
from rwini import *

global begin
global rec
# 录音类
class Recorder():
    def __init__(self, chunk=1024, channels=2, rate=48000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
 
   
    def findInternalRecordingDevice_兼容状态(self, p): #pyaudio不乱码用这个
        target = '立体声混音'
        for i in range(p.get_device_count()):
            devInfo = p.get_device_info_by_index(i)
            if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
                #print('已找到内录设备,序号是 ',i)
                return i
        print('无法找到内录设备!')
        return -1

    def findInternalRecordingDevice(self, p): #pyaudio要乱码用这个,用之前先运行一次 check_audio_device.py
        getnum = 读配置项("dev.ini", "setdev", "id", )
        return(int(getnum))
 
    # 开始录音，开启一个新线程进行录音操作
    def start(self):
        threading._start_new_thread(self.__record, ())
 

    # 执行录音的线程函数
    def __record(self):
        global begin
        self._running = True
        self._frames = []
 
        p = pyaudio.PyAudio()
        # 查找内录设备
        dev_idx = self.findInternalRecordingDevice(p)
        if dev_idx < 0:
            return
        # 在打开输入流时指定输入设备
        stream = p.open(input_device_index=dev_idx,
                        format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        # 循环读取输入流
        while (self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
            if(time.time() - begin > 10):##########################################音频截取时长
               del self._frames[0]
            #print(int(time.time() - begin), len(self._frames))

        # 停止读取输入流
        stream.stop_stream()
        # 关闭输入流
        stream.close()
        # 结束pyaudio
        p.terminate()
        return
 
    # 停止录音
    def stop(self):
        self._running = False
 
    # 保存到文件
    def save(self, fileName):
        # 创建pyAudio对象
        p = pyaudio.PyAudio()
        # 打开用于保存数据的文件
        wf = wave.open(fileName, 'wb')
        # 设置音频参数
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        # 写入数据
        wf.writeframes(b''.join(self._frames))
        # 关闭文件
        wf.close()
        # 结束pyaudio
        p.terminate()
 
def get_aud():
    global rec
    fname = "./temp/" + str(random.randint(10000, 99999)) + ".wav"
    rec.save(fname)
    myio = io.BytesIO()
    with open(fname, "rb") as fi:
        myio = io.BytesIO(fi.read())
    os.remove(fname)
    return(myio)

rec = Recorder()

if not os.path.exists('temp'):
    os.makedirs('temp')
 
begin = time.time()
 
rec.start()

#time.sleep(10)
#rec.save("./temp/sample.wav")