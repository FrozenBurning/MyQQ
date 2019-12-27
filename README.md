# 基于中央定位服务器的P2P聊天系统
## Computer Network Project 2019

Developed based on Python and PyQt5, a fancy P2P online chat application.

**Author: 陈昭熹 2017011552**


**Features**:

- 使用TCP流socket实现用户之间的网络连接和数据交换
- 基于中央服务器实现账户上线下线
- 维护通讯录，实时更新好友状态
- P2P文字通信
- 友好的用户界面
- 支持音视频通话
- 创新地使用路由式线程管理(基于Producter-Consumer模式)


### Shortcut

##### 实验报告

See [report.pdf](report/report.pdf)
Latex source code at [report.tex](report/report.tex)

##### 文件目录

- 与中央服务器的连接工具 [connectiontool.py](utility/connectiontool.py)
- 基础监听及套接字 [listener.py](Chatter/listener.py)
- 基础发送及套接字 [sender.py](Chatter/sender.py)
- 线程“路由” [router.py](Chatter/router.py)
- 面向用户的主线程 [user.py](Chatter/user.py)
- 音视频发送 [clientMedia.py](utility/clientMedia.py)
- 音视频监听及接受 [serverMedia.py](utility/serverMedia.py)
- 数据协议的某些字段定义 [data_type.py](Chatter/data_type.py)
- 程序入口 [main.py](main.py)


## 1.Prerequisites

运行环境及源码脚本运行库支持，若可执行文件无法运行，请阅读以下部分。

### 1.1 OS

Ubuntu 18.04 LTS

### 1.2 Python 3.6

Python3相关版本均可，不支持Python2

### 1.3 Related Library(Optional取决于你的环境)

是否使用sudo取决于你的本地环境

```bash
(sudo) pip3 install pyinstaller
(sudo) pip3 install PyQt5
(sudo) apt-get install portaudio19-dev python3-pyaudio
(sudo) apt-get install python-opencv
```

## 2. Usage

以下方式任选其一进行运行，如果是正常linux环境，推荐可执行文件方式，理论上无需额外配置，相应库已经在build中打包提供。

### 2.1 可执行文件方式

可执行文件在/dist目录下，运行如下指令:
```bash
cd path-to-project
./dist/main
```

### 2.2 脚本执行方式

在工程当前目录下执行main.py即可，命令如下：
```bash
cd path-to-project
python3 main.py
```

### 2.3 本地配置环境后(见前一节),生成可执行文件方式

配置好环境后,参考上一章节,执行如下命令:
```bash
pyinstaller -F main.py
```
会在dist目录下生成可执行文件