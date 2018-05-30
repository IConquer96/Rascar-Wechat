# -*- coding: utf-8-*-

from player import Player
import sys
from imp import reload

reload(sys)
#定义播放器
player = Player()

def say(what):
#配置账户信息

	from aip import AipSpeech
	""" 你的 APPID AK SK """
	APP_ID = '10462370'
	API_KEY = '*************************'
	SECRET_KEY = '*****************************'
	client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

	result  = client.synthesis( what, 'zh', 1, {
		'vol': 5,
		'per': 3,
	})
	# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
	if not isinstance(result, dict):
		with open('tts.mp3', 'wb') as f:
			f.write(result)
	player.play('file://{}'.format('/home/pi/wechat/tts.mp3'))

if __name__ == '__main__':
	say('李博是最最最帅的')
