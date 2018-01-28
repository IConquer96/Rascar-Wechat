#!/usr/bin/python
# -*- coding:utf-8 -*-
import itchat
import wifirobots as robot
from player import Player
import RPi.GPIO as GPIO
import shutil
import os
import sys
import time
import re
import subprocess
from itchat.content import *
from imp import reload

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

player = Player()

@itchat.msg_register(TEXT,isFriendChat=True)
def text_reply(msg):
    #itchat.send('%s: %s' % (msg['Type'],msg['Text']),msg['FromUserName'])
    command = msg['Text']
    #lo=msg['ToUserName']
    FROMNAME = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    if msg['ToUserName'] == 'filehelper':  #判断是不是发给文件传输助手
        TONAME = FROMNAME         #相当于是发给自己的
        #os.system('echo "%s" >laji.txt' % command)
        #os.system('"%s" >linux_echo.txt' % command)
        #p=subprocess.Popen("%s >linux_echo.txt" % command,shell=True)
        #time.sleep(1)
        #p.kill()
        #print (p)
        #os.system('echo "%s" >xiao.txt' % p)
        for line in open("/home/pi/wechat/linux_echo.txt"):
            itchat.send_msg(msg=line,toUserName='filehelper')
        #itchat.send_file("/home/pi/dai/command/linux_echo.txt",toUserName='filehelper')
        if command.find(u"开") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
            print ("打开前大灯")
            robot.Open_Flight()
            GPIO.output(LED_CTR, GPIO.HIGH)
            shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_on_light.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
        elif command.find(u"关") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
                print ("关闭前大灯")
                robot.Close_Flight()
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_off_light.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"前") !=-1 and command.find(u"进") !=-1:
                print ("前进")
                robot.Motor_Forward()
                time.sleep(2)
                robot.Motor_Stop()
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/forward.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"后") !=-1 and command.find(u"退") !=-1:
                print ("后退")
                robot.Motor_Backward()
                time.sleep(2)
                robot.Motor_Stop()
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/backward.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"左") !=-1 and command.find(u"转") !=-1:
                print ("左转")
                robot.Motor_TurnLeft()
                p = GPIO.PWM(11, 3)
                p.start(20)
                time.sleep(0.5)
                p.stop()
                robot.Motor_Stop()
                GPIO.output(11, GPIO.LOW)
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_left.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"右") !=-1 and command.find(u"转") !=-1:
                print ("右转")
                robot.Motor_TurnRight()
                p = GPIO.PWM(8, 3)
                p.start(20)
                time.sleep(0.5)
                p.stop()
                robot.Motor_Stop()
                GPIO.output(8, GPIO.LOW)
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_right.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"黑") !=-1 and command.find(u"线") !=-1:
                print ("黑线")
                robot.TrackLine()
        #os.system("/home/pi/DuerOS-Python-Client/temp.mp3")
        player.play('file://{}'.format('/home/pi/DuerOS-Python-Client/temp.mp3'))
    else:         #根据ToUserName的ID号来搜索对应的微信昵称
        TONAME = itchat.search_friends(userName=msg['ToUserName'])['NickName']
    today = time.strftime('  %m-%m-%d  %H:%M:%S', time.localtime())
    xie = FROMNAME + '-->' + TONAME +today
    #print (xie)
    #print (command)



@itchat.msg_register([NOTE])
def text_reply(msg):
    # 微信里，每个用户和群聊，都使用很长的ID来区分
    # msg['FromUserName']就是发送者的ID
    # 将消息的类型和文本内容返回给发送者
    itchat.send("note dai",toUserName='filehelper')

    #itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
	
	

@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO,SHARING])
def download_files(msg):
    if msg['ToUserName'] == 'filehelper':
        msg['Text'](msg['FileName'])

reload(sys)
#sys.setdefaultencoding('utf8')
itchat.auto_login(enableCmdQR=2,hotReload=True)  #使能命令行验证登陆，以及登陆后免验证
itchat.send("tom dai yi long",toUserName='filehelper')
itchat.run()
