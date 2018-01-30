# Rascar-Wechat
一个很酷的项目，可以在微信上给文件助手（可以自定义为其他任何好友、群聊、公众号）发文本或者语音消息，来控制树莓派智能小车的前进后退、以及与智能小车进行对话等等，会持续更新功能，欢迎Fork。

#itchat
itchat是一个开源的微信个人号接口，使用python调用微信从未如此简单。可以通过它进行微信消息的读取，回复，联系人的读取等等
### 1. 安装
    pip install itchat
### 2. 简单入门
####1.登陆配置
登陆使用的是itchat提供了auto_login方法，调用即可完成登录。
一般而言，会在完成消息的注册之后再进行登陆。
这里需要特别强调的是两点，分别是**短时间关闭重连**、**命令行二维码**。
* itchat提供了登陆状态暂存，关闭程序后一定时间内不需要扫码即可登录。由于目前微信网页版提供上一次登录的微信号不扫码直接手机确认登陆，所以如果开启登陆状态暂存将会自动使用这一功能。
* 为了方便在无图形界面使用itchat，程序内置了命令行二维码的显示。

#####短时间关闭程序后重连
这样即使程序关闭，一定时间内重新开启也可以不用重新扫码。
最简单的用法就是给auto_login方法传入值为真的hotReload。
该方法会生成一个静态文件itchat.pkl，用于存储登陆的状态。
```
import itchat
from itchat.content import TEXT

@itchat.msg_register(TEXT)
def simple_reply(msg):
    print(msg.text)

itchat.auto_login(hotReload=True)
itchat.run()
```
#####命令行二维码显示
通过以下命令可以在登陆的时候使用命令行显示二维码：

    itchat.auto_login(enableCmdQR=True)
部分系统可能字幅宽度有出入，可以通过将enableCmdQR赋值为特定的倍数进行调整：如部分的linux系统，块字符的宽度为一个字符（正常应为两字符），故赋值为2

    itchat.auto_login(enableCmdQR=2)

####2.聊天对象
在使用个人微信的过程当中主要有三种账号需要获取，分别为：
* 好友
* 公众号
* 群聊

itchat为这三种账号都提供了整体获取方法与搜索方法。群聊**多出获取用户列表方法以及创建群聊、增加、删除用户的方法**。
接下来对三种分别介绍如何使用以及如何通过唯一的Uin确定好友与群聊。
#####好友
好友的获取方法为get_friends，将会返回完整的好友列表。
* 其中每个好友为一个**字典**
* 列表的第一项为本人的账号信息
* 传入update键为True将可以更新好友列表并返回

好友的搜索方法为search_friends，有四种搜索方式：
1.  仅获取自己的用户信息
2.  获取特定UserName的用户信息 
3.  获取备注、微信号、昵称中的任何一项等于name键值的用户
4.  获取备注、微信号、昵称分别等于相应键值的用户

下面是示例程序：

获取自己的用户信息，返回自己的属性字典

    itchat.search_friends()
获取特定UserName的用户信息

    itchat.search_friends(userName='@abcdefg1234567')
获取任何一项等于name键值的用户

    itchat.search_friends(name='littlecodersh')
获取分别对应相应键值的用户

    itchat.search_friends(wechatAccount='littlecodersh')
其中3、4项功能可以一同使用，将返回同时满足两个条件的好友

    itchat.search_friends(name='LittleCoder机器人', wechatAccount='littlecodersh')
更新用户信息的方法为update_friend。
* 该方法需要传入用户的UserName，返回指定用户的最新信息
* 也可以传入UserName组成的列表，那么相应的也会返回指定用户的最新信息组成的列表


    memberList = itchat.update_friend('@abcdefg1234567')
#####公众号
公众号的获取方法为get_mps，将会返回完整的公众号列表。
* 其中每个公众号为一个**字典**
* 传入update键为True将可以更新公众号列表并返回

公众号的搜索方法为search_mps，有两种搜索方法：
1. 获取特定UserName的公众号
2. 获取名字中含有特定字符的公众号

如果两项都做了特定，将会仅返回特定UserName的公众号，下面是示例程序：

获取特定UserName的公众号，返回值为一个字典

    itchat.search_mps(userName='@abcdefg1234567')
获取名字中含有特定字符的公众号，返回值为一个字典的列表

    itchat.search_mps(name='LittleCoder')
以下方法相当于仅特定了UserName

    itchat.search_mps(userName='@abcdefg1234567', name='LittleCoder')
#####群聊
群聊的获取方法为get_chatrooms，将会返回完整的群聊列表。
* 其中每个群聊为一个字典
* 传入update键为True将可以更新群聊列表并返回通讯录中保存的群聊列表
* 群聊列表为后台自动更新，如果中途意外退出存在极小的概率产生本地群聊消息与后台不同步
* 为了保证群聊信息在热启动中可以被正确的加载，即使不需要持续在线的程序也需要运行`itchat.run()`
* 如果不想要运行上述命令，请在退出程序前调用`itchat.dump_login_status()`，更新热拔插需要的信息

群聊的搜索方法为search_chatrooms，有两种搜索方法：
1. 获取特定UserName的群聊
2. 获取名字中含有特定字符的群聊

如果两项都做了特定，将会仅返回特定UserName的群聊，下面是示例程序：

获取特定UserName的群聊，返回值为一个字典

    itchat.search_chatrooms(userName='@@abcdefg1234567')
获取名字中含有特定字符的群聊，返回值为一个字典的列表

    itchat.search_chatrooms(name='LittleCoder')
以下方法相当于仅特定了UserName

    itchat.search_chatrooms(userName='@@abcdefg1234567', name='LittleCoder')
群聊用户列表的获取方法为update_chatroom。
* 如果想要更新该群聊的其他信息也可以用该方法
* 群聊在首次获取中不会获取群聊的用户列表，需要调用该命令才能获取群聊的成员
* 该方法需要传入群聊的UserName，返回特定群聊的详细信息
* 也可以传入UserName组成的列表，那么相应的也会返回指定用户的最新信息组成的列表


    memberList = itchat.update_chatroom('@@abcdefg1234567', detailedMember=True)
创建群聊、增加、删除群聊用户的方法如下所示：
* 由于之前通过群聊检测是否被好友拉黑的程序，目前这三个方法都被严格限制了使用频率
* 删除群聊需要本账号为群管理员，否则会失败
* 将用户加入群聊有直接加入与发送邀请，通过useInvitation设置
* 超过40人的群聊**无法使用**直接加入的加入方式，特别注意
```
memberList = itchat.get_friends()[1:]
chatroomUserName = itchat.create_chatroom(memberList, 'test chatroom') # 创建群聊，topic键值为群聊名
itchat.delete_member_from_chatroom(chatroomUserName, memberList[0]) # 删除群聊内的用户
itchat.add_member_into_chatroom(chatroomUserName, memberList[0], useInvitation=False) # 增加用户进入群聊
```
#####Uins
Uin 就是微信中用于标识用户的方式，每一个用户、群聊都有唯一且不同的Uin。通过Uin，即使退出了重新登录，也可以轻松的确认正在对话的是上一次登陆的哪一个用户。但注意，Uin与其他值不同，微信后台做了一定的限制，必须通过特殊的操作才能获取。
最简单来说，首次点开登陆用的手机端的某个好友或者群聊，itchat就能获取到该好友或者群聊的Uin。
如果想要通过程序获取，也可以用程序将某个好友或者群聊置顶（取消置顶）。
这里提供一个提示群聊更新的程序：
```
import re, sys, json

import itchat
from itchat.content import *

itchat.auto_login(True)

@itchat.msg_register(SYSTEM)
def get_uin(msg):
    if msg['SystemInfo'] != 'uins': return
    ins = itchat.instanceList[0]
    fullContact = ins.memberList + ins.chatroomList + ins.mpList
    print('** Uin Updated **')
    for username in msg['Text']:
        member = itchat.utils.search_dict_list(
            fullContact, 'UserName', username)
        print(('%s: %s' % (
            member.get('NickName', ''), member['Uin']))
            .encode(sys.stdin.encoding, 'replace'))

itchat.run(True)
```
每当Uin更新了，就会打印相应的更新情况。

####3.消息处理
#####消息内容
微信初始化消息、文本消息、图片消息、小视频消息、地理位置消息、名片消息、语音消息、动画表情、普通链接或应用分享消息、音乐链接消息、群消息、红包消息、系统消息
#####回复方法
*   方法：

```
send(msg='Text Message', toUserName=None)
```

*   所需值：
    *   msg：消息内容
    *   '@fil@文件地址'将会被识别为传送文件
    *   '@img@图片地址'将会被识别为传送图片
    *   '@vid@视频地址'将会被识别为小视频
    *   toUserName：发送对象，如果留空将会发送给自己
*   返回值：发送成功->True, 失败->False
*   程序示例：使用的素材可以在[这里](http://7xrip4.com1.z0.glb.clouddn.com/ItChat/%E4%B8%8A%E4%BC%A0%E7%B4%A0%E6%9D%90.zip)下载
```
#coding=utf8
import itchat

itchat.auto_login()
itchat.send('Hello world!')
# 请确保该程序目录下存在：gz.gif以及xlsx.xlsx
itchat.send('@img@%s' % 'gz.gif')
itchat.send('@fil@%s' % 'xlsx.xlsx')
itchat.send('@vid@%s' % 'demo.mp4')
```
####4.注册方法
itchat将根据接收到的消息类型寻找对应的已经注册的方法。如果一个消息类型没有对应的注册方法，该消息将会被舍弃。
#####注册
可以通过两种方式注册消息方法
```
import itchat
from itchat.content import *

# 不带具体对象注册，将注册为普通消息的回复方法
@itchat.msg_register(TEXT)
def simple_reply(msg):
    return 'I received: %s' % msg['Text']

# 带对象参数注册，对应消息对象将调用该方法
@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
def text_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))
```
#####消息类型
向注册方法传入的msg包含微信返回的字典的所有内容。

本api增加Text、Type（也就是参数）键值，方便操作。

itchat.content中包含所有的消息类型参数，内容如下表所示：

参数|类型|Text键值
:-:|:-:|:-:
TEXT|文本|文本内容
MAP|地图|位置文本
CARD|名片|推荐人字典
NOTE|通知|通知文本
SHARING|分享|分享名称
PICTURE|图片/表情|下载方法
RECORDING|语音|下载方法
ATTACHMENT|附件|下载方法
VIDEO|小视频|下载方法
FRIENDS|好友邀请|添加好友所需参数
SYSTEM|系统消息|更新内容的用户或群聊的UserName组成的列表
比如你需要存储发送给你的附件：
```
@itchat.msg_register(ATTACHMENT)
def download_files(msg):
    msg['Text'](msg['FileName'])
```
值得注意的是，群消息增加了三个键值：

* isAt: 判断是否@本号
* ActualNickName: 实际NickName
* Content: 实际Content

可以通过本程序测试：
```
import itchat
from itchat.content import TEXT

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    print(msg.isAt)
    print(msg.actualNickName)
    print(msg.text)

itchat.auto_login()
itchat.run()
```
#####注册消息的优先级
优先级分别为：后注册消息先于先注册消息，带参数消息先于不带参数消息。

以下面的两个程序为例：
```
import itchat
from itchat.content import *

itchat.auto_login()

@itchat.msg_register(TEXT)
def text_reply(msg):
    return 'This is the old register'

@itchat.msg_register(TEXT)
def text_reply(msg):
    return 'This is a new one'

itchat.run()
```
在私聊发送文本时将会回复This is a new one。
```
import itchat
from itchat.content import *

itchat.auto_login()

@itchat.msg_register
def general_reply(msg):
    return 'I received a %s' % msg.type

@itchat.msg_register(TEXT)
def text_reply(msg):
    return 'You said to me one to one: %s' % msg.text

itchat.run()
```
仅在私聊发送文本时将会回复You said to me one to one，其余情况将会回复I received a ...。
#STT (Speak To Text)
通过上述的itchat模块，就可以在树莓派上用python进行微信的信息接收等，文本消息我们可以利用之前类似的方法进行识别、控制，那么仅仅用文本消息控制就显得不够智能了，需要用语音来控制，那么如何用语音来控制小车呢？这就要用到STT模块，这个模块做的就是把语音识别为文本信息，目前有多家公司有开源项目可以使用，比如Google、百度、讯飞，综合考虑语音识别准确率、易用性上，我选择了百度的API接口。
###百度AI平台
要想使用百度的语音识别API，有如下几个准备工作。
1. 首先要成为百度开发者
2. 创建应用
3. 获取密钥
4. 合成Access Token

前三部分可以在百度开发者平台上很简单的注册申请，不再赘述。要注意的是保留好上述申请到的密钥（API KEY、Secret KEY），会在下面用到；第四部分下面会详细介绍。
###语音识别简介
百度语音识别通过 REST API 的方式给开发者提供一个通用的 HTTP 接口。 上传需要完整的录音文件，录音文件时长不超过60s。
###调用流程
#####1. 获取Access Token
**请求URL数据格式**
向授权服务地址`https://aip.baidubce.com/oauth/2.0/token`发送请求（推荐使用POST），并在URL中带上以下参数：
* grant_type： 必须参数，固定为client_credentials；
* client_id： 必须参数，应用的API Key；
* client_secret： 必须参数，应用的Secret Key；

**Python获取access_token示例代码**
```
import urllib, urllib2, sys
import ssl

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content= response.read()
if (content):
    print(content)
```
上述代码中content是一个JSON格式信息，其中包含你请求到的授权码，会在调用API时用到，有限期一般为一个月。
**服务器返回的JSON文本参数如下**：
* access_token： 要获取的Access Token；
* expires_in： Access Token的有效期(秒为单位，一般为1个月)；
* 其他参数忽略，暂时不用;
例如：
```
{
  "access_token": "25.b55fe1d287227ca97aab219bb249b8ab.315360000.1798284651.282335-8574074",
  "expires_in": 2592000,
  "scope": "public wise_adapt",
  "session_key": "9mzdDZXu3dENdFZQurfg0Vz8slgSgvvOAUebNFzyzcpQ5EnbxbF+hfG9DQkpUVQdh4p6HbQcAiz5RmuBAja1JJGgIdJI",
  "access_token": "24.6c5e1ff107f0e8bcef8c46d3424a0e78.2592000.1485516651.282335-8574074",
  "session_secret": "dfac94a3489fe9fca7c3221cbf7525ff"
}
```
其中`access_token`即为我们需要的信息，通过Python的`json`模块，把它提取出来。
```
data = json.loads(content)
token = data["access_token"]
```
#####2. 请求方式
* 如果音频在本地，需要将音频数据放在body中。（推荐方式）
* 如果音频在互联网上，可以让百度服务器下载，然后回调到自己服务器的接口
* 音频在本地，有JSON和raw两种方式提交。
* 音频在在互联网上，需要百度服务器下载，只能通过JSON方式提交

这里只介绍通过json 方式，上传本地文件（官方推荐，更高效）
######JSON方式上传
语音数据和其他参数通过标准 JSON 格式串行化 POST 上传， JSON 里包括的参数：

字段名|是必填或选填|描述
:-:|:-:|:-:
format|必填|语音文件的格式，pcm 或者 wav 或者 amr。不区分大小写。推荐pcm文件
rate|必填|采样率， 8000 或者 16000， 推荐 16000 采用率
channel|必填|声道数，仅支持单声道，请填写固定值 1
cuid|必填|用户唯一标识，用来区分用户，计算UV值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内。
token|必填|开放平台获取到的开发者[ access_token](http://yuyin.baidu.com/docs/tts/135#获取 Access Token "access_token")
lan|选填|语种选择，默认中文（zh）。 中文=zh、粤语=ct、英文=en，不区分大小写
url|选填|可下载的语音下载地址，与callback连一起使用，确保百度服务器可以访问。
callback|选填|用户服务器的识别结果回调地址，确保百度服务器可以访问
speech|选填|本地语音文件的的二进制语音数据 ，需要进行base64 编码。与len参数连一起使用。
len|选填|本地语音文件的的字节数，单位字节

######上传示例(speech, len 参数)
JSON格式POST上传本地文件,固定头部`header:Content-Type:application/json`,4K大小的pcm文件（普通话录音）请求： speech 参数填写为文件内容base64后的结果：
```
{
	"format":"pcm",
	"rate":16000,
	"channel":1,
	"token":xxx,
	"cuid":"baidu_workshop",
	"len":4096,
	"speech":"xxx", // xxx为 base64（FILE_CONTENT）
}
```
######返回示例
```
{
    "corpus_no":"6433214037620997779",
    "err_msg":"success.",
    "err_no":0,
    "result":["北京科技馆，"],
    "sn":"371191073711497849365"
}
```
######注意事项
* len 字段表示原始语音大小字节数，不是 base64 编码之后的长度。

#TTS(Text To Speak)
智能小车识别命令做出相应动作后要进行反馈，同样采用百度的语音合成API，将要说的话合称为语音，这部分我们采用与上面的REST API不同的方式，采用Python SDK的方式获取。
###安装语音合成 Python SDK
语音合成 Python SDK目录结构
```
├── README.md
├── aip                   //SDK目录
│   ├── __init__.py       //导出类
│   ├── base.py           //aip基类
│   ├── http.py           //http请求
│   └── speech.py //语音合成
└── setup.py              //setuptools安装
```
安装使用Python SDK有如下方式：
* 如果已安装pip，执行pip install baidu-aip即可。
* 如果已安装setuptools，执行python setup.py install即可。

***此种方式比较简单，不做详细介绍***

#控制代码
这部分在教程[人工智能-树莓派小车（4）——通过语音玩转智能小车](https://www.jianshu.com/p/62f249fa74bc)已经介绍过，原理相同。

# 语音聊天
语音聊天国内做的比较好的有图灵机器人、小i机器人，百度的小度也不错，不过还没有什么开放接口，所以目前在使用图灵机器人（采用WEB API 2.0 接口），下面简单介绍一下申请、使用方法等基本流程。
### 简介
图灵机器人API是在人工智能的核心能力（包括语义理解、智能问答、场景交互、知识管理等）的基础上，为广大开发者、合作伙伴和企业提供的一系列基于云计算和大数据平台的在线服务和开发接口。
开发者可以利用图灵机器人的API创建各种在线服务，灵活定义机器人的属性、编辑机器人的智能问答内容，打造个人专属智能交互机器人。
### 使用流程
##### 注册申请图灵帐号
登录图灵机器人官方网站[http://www.tuling123.com/](http://www.tuling123.com/)，点击右上角“注册”按钮进行注册并激活帐号，如下图所示：
![注册申请图灵帐号](http://upload-images.jianshu.io/upload_images/9918121-ab3c05ff53fca6b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##### 获取APIKEY

每一个激活用户都可以通过图灵机器人开放平台获取多个APIKEY（当前每个用户可最多获取5个APIKEY），用户可以根据自己的需要获取不同的图灵APIKEY来应用于多种场景，获取成功后就等于拿到了开启图灵服务的钥匙。
登录图灵帐号，进入个人中心，在“我的机器人》机器人详情》接入”页面即可看到每一个机器人的API KEY，如下图所示：
![获取APIKEY](http://upload-images.jianshu.io/upload_images/9918121-ec6086136c095db6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
##### 编码方式
    UTF-8（调用图灵API的各个环节的编码方式均为UTF-8）
##### 接口地址

    http://openapi.tuling123.com/openapi/api/v2

##### 请求方式

    HTTP POST

##### 请求参数

请求参数格式为 json
请求示例：

```
{
	"reqType":0,
    "perception": {
        "inputText": {
            "text": "附近的酒店"
        },
        "inputImage": {
            "url": "imageUrl"
        },
        "selfInfo": {
            "location": {
                "city": "北京",
                "province": "北京",
                "street": "信息路"
            }
        }
    },
    "userInfo": {
        "apiKey": "",
        "userId": ""
    }
}

```

**参数说明**

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| reqType | int | N | - | 输入类型:0-文本(默认)、1-图片、2-音频 |
| perception | - | Y | - | 输入信息 |
| userInfo | - | Y | - | 用户参数 |

**perception**

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| inputText | - | N | - | 文本信息 |
| inputImage | - | N | - | 图片信息 |
| inputMedia | - | N | - | 音频信息 |
| selfInfo | - | N | - | 客户端属性 |

注意：输入参数必须包含inputText或inputImage或inputMedia！

***inputText***

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| text | String | Y | 1-128字符 | 直接输入文本 |

***inputImage***

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| url | String | Y |  | 图片地址 |

***inputMedia***

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| url | String | Y |  | 音频地址 |

***selfInfo***

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| location | - | N | - | 地理位置信息 |

***location***

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| city | String | Y | - | 所在城市 |
| province | String | N | - | 省份 |
| street | String | N | - | 街道 |

**userInfo**

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| apiKey | String | Y | 32位 | 机器人标识 |
| userId | String | Y | 长度小于等于32位 | 用户唯一标识 |
| groupId | String | N | 长度小于等于64位 | 群聊唯一标识 |
| userIdName | String | N | 长度小于等于64位 | 群内用户昵称 |

##### 输出参数

输出示例：

```
  {
    "intent": {
        "code": 10005,
        "intentName": "",
        "actionName": "",
        "parameters": {
            "nearby_place": "酒店"
        }
    },
    "results": [
        {
         	"groupType": 1,
            "resultType": "url",
            "values": {
                "url": "http://m.elong.com/hotel/0101/nlist/#indate=2016-12-10&outdate=2016-12-11&keywords=%E4%BF%A1%E6%81%AF%E8%B7%AF"
            }
        },
        {
         	"groupType": 1,
            "resultType": "text",
            "values": {
                "text": "亲，已帮你找到相关酒店信息"
            }
        }
    ]
}

```

参数说明

| 参数 | 类型 | 是否必须 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| intent | - | Y | - | 请求意图 |
| results | - | N | - | 输出结果集 |

**intent**

| 参数 | 类型 | 是否包含 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| code | int | Y | - | 输出功能code |
| intentName | String | N | - | 意图名称 |
| actionName | String | N | - | 意图动作名称 |
| parameters | String | N | - | 功能相关参数 |

**results**

| 参数 | 类型 | 是否包含 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| resultType | String | Y | 文本(text);连接(url);音频(voice);视频(video);图片(image);图文(news) | 输出类型 |
| values | - | Y | - | 输出值 |
| groupType | int | Y | - | ‘组’编号:0为独立输出，大于0时可能包含同组相关内容 (如：音频与文本为一组时说明内容一致) |


