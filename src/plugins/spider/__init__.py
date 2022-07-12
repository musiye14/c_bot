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



#  ������¼cookies����ŵ�  0-bilibili
cookie_list=['0']




# �ж�һ��cookies.josn�Ĵ�����
if not os.path.exists('src/plugins/spider/cookies.json'):
	x=dict()
	with open("src/plugins/spider/cookies.json",'w')as f:
		json.dump(x,f)



@change_ccokies.handle()
async def c_cookies_1(event:Event,bot:Bot,matcher:Matcher, args:Message = CommandArg()):
	plain_text = args.extract_plain_text()  # �״η�������ʱ����Ĳ���������/���� �Ϻ�����argsΪ�Ϻ�
	if plain_text:
		matcher.set_arg("number", args)  # ����û������˲�����ֱ�Ӹ�ֵ
	# await bot.send(event,message='��������ţ�0-bվ')
	# print(f"\n{args}\n")

@change_ccokies.got("number",prompt="��������ţ�0-bվ")
async def c_cookies_2(event:Event,bot:Bot,matcher:Matcher,number: Message = Arg(),Number:str = ArgPlainText("number")):
	print(f"\n{Number}\n")
	if(Number not in cookie_list):
		await change_ccokies.reject(number.template("�����ѯ����� {number} �ݲ�֧�֣����������룡"))
@change_ccokies.got("cookie", prompt="������cookies")
async def c_cookies_3(event:Event,bot:Bot,matcher:Matcher,cookie: Message = Arg(),Number: str = ArgPlainText("number")):
	print(f"\n{Number}\n")
	print(f"\n{'0'==Number}\n")
	if(Number=='0'):
		with open("src/plugins/spider/cookies.json",'r')as f:
			cookies_dict=json.load(f)

		cookies_dict['bilibili']=str(cookie)
		with open('src/plugins/spider/cookies.json','w')as f:
			json.dump(cookies_dict,f)

		print("cookies�õ�����  "+cookie)
		await bot.send_private_msg(user_id='1950655144', message="cookies�ѱ���")
		await spider_b()
	else:
		await bot.send_private_msg(user_id='1950655144', message="��Ŵ���")
	return


# @spider.handle()
# async def bi(event:Event,bot:Bot):
# 	with open("src/plugins/spider/cookies.json",'r')as f:
# 		cookie_dict=json.load(f)
# 	if(cookie_dict.get('bilibili')!=None):
# 		#��ʾһ��Ҫcookies
# 		await bot.send_private_msg(user_id='1950655144', message="������cookiesȥ����cookies")
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
# 	# ����һ����cookie תcookiejar�ĺ���
# 	def extract_cookiejar(cookie):
# 		cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
# 		return cookies
#
# 	cookie_dir = extract_cookiejar(cookie)
#
# 	cookiejar = requests.utils.cookiejar_from_dict(cookie_dir)
#
# 	# ��session����cookie����
# 	session.cookies = cookiejar
#
# 	bilibili_manhua_qiandao_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
# 	bilibili_manhua_qiandaoxinxi_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo'
# 	# ������ҳ����ǩ��ͷ��Ϣ
# 	bilibili_manhua_response = session.post(bilibili_manhua_qiandao_url, headers=headers, data=Body)
# 	# ��ȡǩ�������ı�
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
# 		msg = 'ǩ���ɹ�������' + str(day_count) + '��ǩ��\n''��������' + str(points) + '��'
# 	elif status == 1:
# 		msg = '�Ѿ�ǩ��������' + str(day_count) + '��ǩ��\n''��������' + str(points) + '��'
# 	else:
# 		msg = 'ǩ��ʧ��,������cookiesʧЧ������������cookies'
# 	await bot.send_private_msg(user_id='1950655144', message=msg)
# 	return





@scheduler.scheduled_job('cron', hour="11", minute="59", id="1")
async def spider_b():
	bot = get_bot()
	with open('src/plugins/spider/cookies.json','r')as f:
		data=json.load(f)
		if (data.get('bilibili') == None):
			# ��ʾһ��Ҫcookies
			await bot.send_private_msg(user_id='1950655144', message="������cookiesȥ����cookies")
			return
	print(data)
	cookie =data['bilibili']

	headers = {
		'User-Agent': 'Mozilla/5.0 BiliComic/2.10.0'
	}
	Body = {"platform": "android"}
	session = requests.session()
	SCKEY = 'SCT15277TKlrhzjwElexzNJAFh3R05LFu'

	#����һ����cookie תcookiejar�ĺ���
	def extract_cookiejar(cookie):
		cookies = dict([l.split("=",1)for l in cookie.split("; ")])
		return cookies

	cookie_dir = extract_cookiejar(cookie)

	cookiejar = requests.utils.cookiejar_from_dict(cookie_dir)

	#��session����cookie����
	session.cookies = cookiejar

	bilibili_manhua_qiandao_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
	bilibili_manhua_qiandaoxinxi_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo'
	bilibili_manhua_user_info_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/GetUserPoint'
	#������ҳ����ǩ��ͷ��Ϣ
	bilibili_manhua_response = session.post(bilibili_manhua_qiandao_url,headers=headers,data=Body)
	#��ȡǩ�������ı�
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
		msg='ǩ���ɹ�������'+str(day_count)+'��ǩ��\n''��������'+str(points)+'��'
	elif status == 1:
		msg='�Ѿ�ǩ��������'+str(day_count)+'��ǩ��\n''��������'+str(points)+'��'
	else:
		msg='ǩ��ʧ��,������cookiesʧЧ������������cookies'
	await bot.send_private_msg(user_id='1950655144', message=msg)



	#�Զ���Ʊ
	# locale.setlocale(locale.LC_CTYPE, 'chinese')
	# ���Լ�����Ϣ
	user_info = session.post(bilibili_manhua_user_info_url, headers=headers, data=Body)
	user_data = user_info.content.decode()
	uesr_info_list = json.loads(user_data)
	print(uesr_info_list)
	# �Լ��ĵ�ǰ����
	user_point = int(uesr_info_list['data']['point'])
	while time.strftime('%H:%M') <="12:01 " and user_point>=100: #�ж�һ��ʱ��  ��10��
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
		await bot.send_private_msg(user_id='1950655144', message=f'�����С���������\n������Ϊ{msg}') #��Ϣ֪ͨ
		return