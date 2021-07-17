from system_hotkey import SystemHotkey
import threading

def some_func(self, hotkey, args):
    print(self, hotkey, args)
    print(4)

def s():
    hk = SystemHotkey(consumer=some_func)
    hk.register(("alt", "s"), 1, 2, 3, 4)

threading._start_new_thread(s, ())


import time
time.sleep(100)