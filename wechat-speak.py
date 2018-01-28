#!/usr/bin/python
# -*- coding:utf-8 -*-
import itchat
import random
import wifirobots as robot
from player import Player
import RPi.GPIO as GPIO
import urllib.request
import json
import base64
import os
import sys
import time
import re
import subprocess
from itchat.content import *
from imp import reload
from Tuling import get_response
from mic import say

#######################################
#############信号引脚定义################
#######################################
GPIO.setmode(GPIO.BCM)

########LED口定义#################
LED_CTR = 5

#######################################
############管脚类型设置及初始化###########
#######################################
GPIO.setwarnings(False)

############led初始化输出模式############
GPIO.setup(LED_CTR,GPIO.OUT,initial=GPIO.LOW)

######################################


# 定义为全局 方便修改
money_receiver = "filehelper"
mycount = ""
#定义播放器
player = Player()

@itchat.msg_register(TEXT,isFriendChat=True)
@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO,SHARING])
def text_reply(msg):
    #itchat.send('%s: %s' % (msg['Type'],msg['Text']),msg['FromUserName'])
    #command = msg['Text']
    #lo=msg['ToUserName']
    FROMNAME = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    if msg['ToUserName'] == 'filehelper':  #判断是不是发给文件传输助手
        TONAME = FROMNAME         #这个其实相当于是发给自己的
        if msg['Type'] == 'Text':
            command = msg['Text']
        if msg['Type'] == 'Recording':
            msg['Text'](msg['FileName'])
            os.system('ffmpeg -y -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 temp.pcm' % msg['FileName'])
            os.remove(msg['FileName'])
            #打开音频文件，并进行编码
            f = open(WAVE_FILE, "rb")
            speech = base64.b64encode(f.read()).decode('utf-8')
            size = os.path.getsize(WAVE_FILE)
            update = json.dumps({"format":WAVE_TYPE, "rate":VOICE_RATE, 'channel':1,'cuid':USER_ID,'token':token,'speech':speech,'len':size}).encode('utf-8')
            update_length = len(update)
            headers = { 'Content-Type' : 'application/json' } 
            url = "http://vop.baidu.com/server_api"
            req = urllib.request.Request(url)
            req.add_header("Content-Type", "application/json")
            req.add_header("Content-Length", update_length)
            
            r = urllib.request.urlopen(url=req, data=update)


            t = r.read().decode('utf-8')
            result = json.loads(t)
            if result['err_msg']=='success.':
                word = result['result'][0].encode('utf-8').decode()
                command = word
                print (word)
                if word!='':
                    if word[len(word)-3:len(word)]=='，':
                        print ( word[0:len(word)-3]  )
                        #itchat.send("%s" % word[0:len(word)-3],toUserName='filehelper')
                        
                    else:
                        print ( word )
                        itchat.send("%s" % word,toUserName='filehelper')
                else:
                    print ( "音频文件不存在或格式错误" )
            else:
                print ( "错误" )
        if command.find(u"开") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
            print ("打开前大灯")
            say(random.choice(['已经帮您开灯','开灯了','好的，开灯','是，正在开灯']))
            robot.Open_Flight()
            GPIO.output(LED_CTR, GPIO.HIGH)
            
        elif command.find(u"关") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
                print ("关闭前大灯")
                say(random.choice(['已经帮您关灯','关灯了','好的，关灯','是，正在关灯']))
                robot.Close_Flight()
                GPIO.output(LED_CTR, GPIO.HIGH)
                
        elif command.find(u"前") !=-1 and command.find(u"进") !=-1:
                print ("前进")
                say(random.choice(['好的，前进','向前出发','是，前进一步']))
                robot.Motor_Forward()
                time.sleep(2)
                robot.Motor_Stop()
                GPIO.output(LED_CTR, GPIO.HIGH)
                
        elif command.find(u"后") !=-1 and command.find(u"退") !=-1:
                print ("后退")
                say(random.choice(['好的，后退','倒车请注意','是，后退一点']))
                robot.Motor_Backward()
                time.sleep(2)
                robot.Motor_Stop()
                GPIO.output(LED_CTR, GPIO.HIGH)
                
        elif command.find(u"左") !=-1 and command.find(u"转") !=-1:
                print ("左转")
                say(random.choice(['好嘞，向左转','拐啦，拐啦，向左拐啦','好的，向左转弯','是，向左转弯']))
                robot.Motor_TurnLeft()
                p = GPIO.PWM(11, 3)
                p.start(20)
                time.sleep(0.5)
                p.stop()
                robot.Motor_Stop()
                GPIO.output(11, GPIO.LOW)
                GPIO.output(LED_CTR, GPIO.HIGH)
                
                
        elif command.find(u"右") !=-1 and command.find(u"转") !=-1:
                print ("右转")
                say(random.choice(['好嘞，向右转','拐啦，拐啦，向右拐啦','好的，向右转弯','是，向右转弯']))
                robot.Motor_TurnRight()
                p = GPIO.PWM(8, 3)
                p.start(20)
                time.sleep(0.5)
                p.stop()
                robot.Motor_Stop()
                GPIO.output(8, GPIO.LOW)
                GPIO.output(LED_CTR, GPIO.HIGH)
                
        elif command.find(u"黑") !=-1 and command.find(u"线") !=-1:
                print ("黑线")
                robot.TrackLine()
        
        elif command == "状态":
            os.system('cat deng.txt door.txt tv.txt >all.txt')
            #user = itchat.search_friends(name=u'等风来')[0]
            itchat.send_file("/home/pi/dai/command/all.txt",toUserName='filehelper')
        else :
            res = get_response(command)
            itchat.send(res or 'I Love You !!!', toUserName='filehelper')
            say(res)

    else:         #根据ToUserName的ID号来搜索对应的微信昵称
        TONAME = itchat.search_friends(userName=msg['ToUserName'])['NickName']
    today = time.strftime('  %Y-%m-%d  %H:%M:%S', time.localtime())
    xie = FROMNAME + '-->' + TONAME +today

time.sleep(1)
reload(sys)
#sys.setdefaultencoding('utf8')
itchat.auto_login(enableCmdQR=2,hotReload=True)  #使能命令行验证登陆，以及登陆后免验证
itchat.send("ok to speak",toUserName='filehelper')


#设置应用信息
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "0Da9pMDM1wHzHgf5muuNN7ohOKr3612g" #填写API Key   需自行申请
client_secret = "iwA59XoFPX2Dn5vtZhzKAbUmYPFKufIO" #填写Secret Key

#合成请求token的URL
url = baidu_server+"grant_type="+grant_type+"&client_id="+client_id+"&client_secret="+client_secret

#获取token
res = urllib.request.urlopen(url).read().decode()
data = json.loads(res)
token = data["access_token"]
print ( token )

#设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
VOICE_RATE = 16000
WAVE_FILE = "16k_dai.pcm" #音频文件的路径
USER_ID = "hail_hydra" #用于标识的ID，可以随意设置
WAVE_TYPE = "pcm"

itchat.run()
