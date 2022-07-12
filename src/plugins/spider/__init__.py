# coding=gbk
import requests
import json
import time
from nonebot.adapters.onebot.v11 import Bot, Message,Event,MessageSegment
from nonebot import require, on_keyword, on_command
from nonebot import get_bot
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText
import locale
import os
import os.path
scheduler = require("nonebot_plugin_apscheduler").scheduler
change_ccokies = on_command("cookies",rule=to_me(),priority=20)
spider=on_command("bi", rule=to_me(), priority=20)



#  用来记录cookies的序号的  0-bilibili
cookie_list=['0']




# 判断一下cookies.josn的存在性
if not os.path.exists('src/plugins/spider/cookies.json'):
	x=dict()
	with open("src/plugins/spider/cookies.json",'w')as f:
		json.dump(x,f)



@change_ccokies.handle()
async def c_cookies_1(event:Event,bot:Bot,matcher:Matcher, args:Message = CommandArg()):
	plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
	if plain_text:
		matcher.set_arg("number", args)  # 如果用户发送了参数则直接赋值
	# await bot.send(event,message='请输入序号：0-b站')
	# print(f"\n{args}\n")

@change_ccokies.got("number",prompt="请输入序号：0-b站")
async def c_cookies_2(event:Event,bot:Bot,matcher:Matcher,number: Message = Arg(),Number:str = ArgPlainText("number")):
	print(f"\n{Number}\n")
	if(Number not in cookie_list):
		await change_ccokies.reject(number.template("你想查询的序号 {number} 暂不支持，请重新输入！"))
@change_ccokies.got("cookie", prompt="请输入cookies")
async def c_cookies_3(event:Event,bot:Bot,matcher:Matcher,cookie: Message = Arg(),Number: str = ArgPlainText("number")):
	print(f"\n{Number}\n")
	print(f"\n{'0'==Number}\n")
	if(Number=='0'):
		with open("src/plugins/spider/cookies.json",'r')as f:
			cookies_dict=json.load(f)

		cookies_dict['bilibili']=str(cookie)
		with open('src/plugins/spider/cookies.json','w')as f:
			json.dump(cookies_dict,f)

		print("cookies拿到的是  "+cookie)
		await bot.send_private_msg(user_id='1950655144', message="cookies已保存")
		await spider_b()
	else:
		await bot.send_private_msg(user_id='1950655144', message="序号错误")
	return


# @spider.handle()
# async def bi(event:Event,bot:Bot):
# 	with open("src/plugins/spider/cookies.json",'r')as f:
# 		cookie_dict=json.load(f)
# 	if(cookie_dict.get('bilibili')!=None):
# 		#提示一下要cookies
# 		await bot.send_private_msg(user_id='1950655144', message="请输入cookies去设置cookies")
# 		return
#
# 	cookie = cookie_list[0]
# 	headers = {
# 		'User-Agent': 'Mozilla/5.0 BiliComic/2.10.0'
# 	}
# 	Body = {"platform": "android"}
# 	session = requests.session()
# 	SCKEY = 'SCT15277TKlrhzjwElexzNJAFh3R05LFu'
#
#
#
# 	# 定义一个把cookie 转cookiejar的函数
# 	def extract_cookiejar(cookie):
# 		cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
# 		return cookies
#
# 	cookie_dir = extract_cookiejar(cookie)
#
# 	cookiejar = requests.utils.cookiejar_from_dict(cookie_dir)
#
# 	# 让session带上cookie访问
# 	session.cookies = cookiejar
#
# 	bilibili_manhua_qiandao_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
# 	bilibili_manhua_qiandaoxinxi_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo'
# 	# 或者网页返回签到头信息
# 	bilibili_manhua_response = session.post(bilibili_manhua_qiandao_url, headers=headers, data=Body)
# 	# 获取签到数据文本
# 	bilibili_data = bilibili_manhua_response.content.decode()
# 	qiandao_list = json.loads((bilibili_data))
# 	bilibili_manhua_qiandaoxinxi_data = session.post(bilibili_manhua_qiandaoxinxi_url, headers=headers).content.decode()
# 	qiandaoxinxi_list = json.loads(bilibili_manhua_qiandaoxinxi_data)
# 	print(qiandaoxinxi_list)
# 	status = qiandaoxinxi_list['data']['status']
# 	day_count = qiandaoxinxi_list['data']['day_count']
# 	points = qiandaoxinxi_list['data']['points'][day_count % 7]
# 	code = qiandao_list['code']
#
#
# 	bot = get_bot()
# 	print(code)
# 	print(status)
# 	if code == 0:
# 		msg = '签到成功，连续' + str(day_count) + '天签到\n''积分增加' + str(points) + '分'
# 	elif status == 1:
# 		msg = '已经签到，连续' + str(day_count) + '天签到\n''积分增加' + str(points) + '分'
# 	else:
# 		msg = '签到失败,可能是cookies失效，请重新设置cookies'
# 	await bot.send_private_msg(user_id='1950655144', message=msg)
# 	return





@scheduler.scheduled_job('cron', hour="11", minute="59", id="1")
async def spider_b():
	bot = get_bot()
	with open('src/plugins/spider/cookies.json','r')as f:
		data=json.load(f)
		if (data.get('bilibili') == None):
			# 提示一下要cookies
			await bot.send_private_msg(user_id='1950655144', message="请输入cookies去设置cookies")
			return
	print(data)
	cookie =data['bilibili']

	headers = {
		'User-Agent': 'Mozilla/5.0 BiliComic/2.10.0'
	}
	Body = {"platform": "android"}
	session = requests.session()
	SCKEY = 'SCT15277TKlrhzjwElexzNJAFh3R05LFu'

	#定义一个把cookie 转cookiejar的函数
	def extract_cookiejar(cookie):
		cookies = dict([l.split("=",1)for l in cookie.split("; ")])
		return cookies

	cookie_dir = extract_cookiejar(cookie)

	cookiejar = requests.utils.cookiejar_from_dict(cookie_dir)

	#让session带上cookie访问
	session.cookies = cookiejar

	bilibili_manhua_qiandao_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
	bilibili_manhua_qiandaoxinxi_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo'
	bilibili_manhua_user_info_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/GetUserPoint'
	#或者网页返回签到头信息
	bilibili_manhua_response = session.post(bilibili_manhua_qiandao_url,headers=headers,data=Body)
	#获取签到数据文本
	bilibili_data = bilibili_manhua_response.content.decode()
	qiandao_list = json.loads((bilibili_data))
	bilibili_manhua_qiandaoxinxi_data = session.post(bilibili_manhua_qiandaoxinxi_url,headers=headers).content.decode()
	qiandaoxinxi_list = json.loads(bilibili_manhua_qiandaoxinxi_data)
	print(qiandaoxinxi_list)
	status = qiandaoxinxi_list['data']['status']
	day_count = qiandaoxinxi_list['data']['day_count']
	points = qiandaoxinxi_list['data']['points'][day_count%7]
	code = qiandao_list['code']

	bot = get_bot()
	if code == 0:
		msg='签到成功，连续'+str(day_count)+'天签到\n''积分增加'+str(points)+'分'
	elif status == 1:
		msg='已经签到，连续'+str(day_count)+'天签到\n''积分增加'+str(points)+'分'
	else:
		msg='签到失败,可能是cookies失效，请重新设置cookies'
	await bot.send_private_msg(user_id='1950655144', message=msg)



	#自动换票
	# locale.setlocale(locale.LC_CTYPE, 'chinese')
	# 拿自己的信息
	user_info = session.post(bilibili_manhua_user_info_url, headers=headers, data=Body)
	user_data = user_info.content.decode()
	uesr_info_list = json.loads(user_data)
	print(uesr_info_list)
	# 自己的当前分数
	user_point = int(uesr_info_list['data']['point'])
	while time.strftime('%H:%M') <="12:01 " and user_point>=100: #判断一手时间  抢10次
		piaozi_list_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/ListProduct?device=h5&platform=web'

		piaozi_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/Exchange?device=h5&platform=web'

		piaozi_list_response = session.post(piaozi_list_url,headers=headers).content.decode()
		data = json.loads(piaozi_list_response)['data'][0]
		id = data['id']
		cost = data['real_cost']

		piaozi_Body = {
			'product_id': id,
			'product_num': 1,
			'point': cost
		}
		piaozi_data = session.post(piaozi_url,headers=headers,data=piaozi_Body).content.decode()
		data = json.loads(piaozi_data)
		msg = data['msg']
		code = data['code']
		await bot.send_private_msg(user_id='1950655144', message=f'购买中。。。。。\n购买结果为{msg}') #信息通知
		return