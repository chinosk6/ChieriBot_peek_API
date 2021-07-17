from rwini import *
import os
import pyaudio
import threading
import wave
import time
from datetime import datetime

global begin
 
# 录音类
class Recorder():
    def __init__(self, chunk=1024, channels=2, rate=48000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
 
    # 获取内录设备序号,在windows操作系统上测试通过，hostAPI = 0 表明是MME设备

 
    # 开始录音，开启一个新线程进行录音操作
    def start(self, devid):
        threading._start_new_thread(self.__record(devid), ())
 
    # 执行录音的线程函数
    def record(self, devid, sec = 5):
        begin = time.time()
        self._running = True
        self._frames = []
 
        p = pyaudio.PyAudio()
        # 查找内录设备
        dev_idx = devid
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
            if(time.time() - begin > sec):
               self._running = False
            #print(time.time() - begin), len(self._frames))

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
 
 
def findInternalRecordingDevice(p = pyaudio.PyAudio()):
    # 要找查的设备名称中的关键字
    #target = '立体声混音'
    # 逐一查找声音设备
    retlist = []
    for i in range(p.get_device_count()):
        devInfo = p.get_device_info_by_index(i)
        retlist.append(devInfo)
        #print(devInfo['name'], i)
        #if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
        #    print('已找到内录设备,序号是 ',i)
        #    return i
    #print('无法找到内录设备!')
    return(retlist)

if __name__ == "__main__":
    rec = Recorder()
    getd = findInternalRecordingDevice()
    #print(getd)
    devid = -1

    for d in getd:
        num = int(d["index"])
        print("设备号" + str(num) + "开始录制,请等待五秒")
        rec.record(num, 5)
        rec.save("record/test_" + str(num) + ".wav")
        print("设备号" + str(num) + "完成录制,请查看效果 - " + "./record/test_" + str(num) + ".wav")
        stat = str(input("设备正确输入y,不正确按任意键"))
        if(stat == 'y'):
            写配置项("dev.ini", "setdev", "id", str(num))
            print("已设置设备号:" + str(num))
            #import sys
            #sys.exit()
            break
    print("已检索完所有设备")