# P2P Chatter Based on Central Server
## Computer Network Project 2019

Developed based on Python and PyQt5, a fancy P2P online chat application.

**Author: Zhaoxi Chen**


**Features**:

- TCP Socket
- Sign in & Sign out
- Contacts
- Text messaging
- Friendly UI
- Media Call
- Threads management based on router-like producer-consumer mode


### Shortcut

##### Report

See [report.pdf](report/report.pdf)
Latex source code at [report.tex](report/report.tex)

##### Files

- To central server [connectiontool.py](utility/connectiontool.py)
- Basic listening socket [listener.py](Chatter/listener.py)
- Basic sending socket [sender.py](Chatter/sender.py)
- Thread manager [router.py](Chatter/router.py)
- Main thread [user.py](Chatter/user.py)
- Media sender [clientMedia.py](utility/clientMedia.py)
- Media listener [serverMedia.py](utility/serverMedia.py)
- Protocol [data_type.py](Chatter/data_type.py)
- UI [mainwindow.py](GUI/mainwindow.py)
- Entrance [main.py](main.py)


## 1.Prerequisites

### 1.1 OS

Ubuntu 18.04 LTS

### 1.2 Python 3.6

not support python2.

### 1.3 Related Library(Optional)

```bash
(sudo) pip3 install pyinstaller
(sudo) pip3 install PyQt5
(sudo) apt-get install portaudio19-dev python3-pyaudio
(sudo) apt-get install python-opencv
```

## 2. Usage

Choose One way to run the application.

### 2.1 Executable

```bash
cd path-to-project
chmod +x ./dist/main
./dist/main
```

### 2.2 Run Script

```bash
cd path-to-project
python3 main.py
```

### 2.3 Package

```bash
pyinstaller -F main.py
```
