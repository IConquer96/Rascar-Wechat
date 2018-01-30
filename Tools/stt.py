# -*- coding: utf-8 -*-
"""
语音识别功能模块(语音输入)
参考：http://open.duer.baidu.com/doc/dueros-conversational-service/device-interface/voice-input_markdown
"""

import urllib.request
import json
import base64


def listen(file):

	os.system('ffmpeg -y -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k_dai.pcm' % file)
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
		return word
	else:
		return '我没有听懂你说什么！！！'

	
#设置应用信息
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "*****************" #填写API Key   需自行申请
client_secret = "****************" #填写Secret Key

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
