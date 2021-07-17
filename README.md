# ChieriBot peek API

- 偷看开发者屏幕,若电脑无公网,需要搭配frp使用
- 支持电脑屏幕、电脑音频以及手机屏幕(Android)



 # 环境

- Python 3
- 安装依赖: `pip install -r requirements.txt`

```
configobj
Flask
Pillow
PyAudio
system-hotkey
waitres
```

- ADB Shell (peek手机屏幕需要)

# 使用

- 启动: `python run.py`

######  - 热键可以在 `run.py`的`s()`函数中自行修改

- 切换公开/私密模式`Alt + s`
- 切换电脑/手机`Alt + c`

# peek !

| 访问地址                          | 功能         | 备注                                                         |
| --------------------------------- | ------------ | ------------------------------------------------------------ |
| example.com/check                 | 检测运行状态 | `GET`,`POST`或`HEAD`                                         |
| example.com/my/getaud             | 获取音频     | 仅电脑                                                       |
| example.com/my/screen?r=`r`&k=`k` | 获取屏幕截图 | `r`为模糊程度,默认值为`2.5`<br>`k`为秘钥,当`r`值低于`2`时必填 |

