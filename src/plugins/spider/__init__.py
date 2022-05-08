# coding=gbk
import requests
import json
import time
from nonebot.adapters.onebot.v11 import Bot, Message,Event,MessageSegment
from nonebot import require, on_keyword, on_command
from nonebot import get_bot
from nonebot.rule import to_me
scheduler = require("nonebot_plugin_apscheduler").scheduler

spider=on_command("bi", rule=to_me(), priority=20)
@spider.handle()
async def call():
	cookie = 'SESSDATA=27d4438d%2C1662653798%2Ce4b6a%2A31; bili_jct=31e06313e087667ffd121dd619485c15;'
	headers = {
		'User-Agent': 'Mozilla/5.0 BiliComic/2.10.0'
	}
	Body = {"platform": "android"}
	session = requests.session()
	SCKEY = 'SCT15277TKlrhzjwElexzNJAFh3R05LFu'

	def pushWechat(code, status, day_count, points):
		localtime = time.strftime("%m/%d-%H:%M:%S");
		ssckey = SCKEY
		send_url = 'http://sctapi.ftqq.com/' + SCKEY + '.send'
		if code == 0 and status != 1:
			params = {
				'title': localtime + 'bilibiliǩ���ɹ�',
				'desp': '����' + str(day_count) + '��ǩ��\n''��������' + str(points) + '��'
			}
		elif status == 1:
			params = {
				'title': localtime + 'bilibili�Ѿ�ǩ����',
				'desp': '����' + str(day_count) + '��ǩ��\n''��������' + str(points) + '��'
			}
		else:
			params = {
				'title': localtime + 'bilibiliǩ��ʧ��',
			}
		data = requests.post(send_url, headers=headers, data=params).content.decode()

	# ����һ����cookie תcookiejar�ĺ���
	def extract_cookiejar(cookie):
		cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
		return cookies

	cookie_dir = extract_cookiejar(cookie)

	cookiejar = requests.utils.cookiejar_from_dict(cookie_dir)

	# ��session����cookie����
	session.cookies = cookiejar

	bilibili_manhua_qiandao_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
	bilibili_manhua_qiandaoxinxi_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo'
	# ������ҳ����ǩ��ͷ��Ϣ
	bilibili_manhua_response = session.post(bilibili_manhua_qiandao_url, headers=headers, data=Body)
	# ��ȡǩ�������ı�
	bilibili_data = bilibili_manhua_response.content.decode()
	qiandao_list = json.loads((bilibili_data))
	bilibili_manhua_qiandaoxinxi_data = session.post(bilibili_manhua_qiandaoxinxi_url, headers=headers).content.decode()
	qiandaoxinxi_list = json.loads(bilibili_manhua_qiandaoxinxi_data)
	print(qiandaoxinxi_list)
	status = qiandaoxinxi_list['data']['status']
	day_count = qiandaoxinxi_list['data']['day_count']
	points = qiandaoxinxi_list['data']['points'][day_count % 7]
	code = qiandao_list['code']

	# pushWechat(code,status,day_count,points)
	bot = get_bot()
	if code == 0:
		msg = 'ǩ���ɹ�������' + str(day_count) + '��ǩ��\n''��������' + str(points) + '��'
	elif status == 1:
		msg = '�Ѿ�ǩ��������' + str(day_count) + '��ǩ��\n''��������' + str(points) + '��'
	else:
		msg = 'ǩ��ʧ��,������cookiesʧЧ������������cookies'
	await bot.send_private_msg(user_id='1950655144', message=msg)
	return





@scheduler.scheduled_job('cron', hour="10", minute="0", id="1")
async def spider_b():
	cookie = 'SESSDATA=27d4438d%2C1662653798%2Ce4b6a%2A31; bili_jct=31e06313e087667ffd121dd619485c15;'
	headers = {
		'User-Agent': 'Mozilla/5.0 BiliComic/2.10.0'
	}
	Body = {"platform": "android"}
	session = requests.session()
	SCKEY = 'SCT15277TKlrhzjwElexzNJAFh3R05LFu'
	def pushWechat(code,status,day_count,points):
		localtime = time.strftime("%m/%d-%H:%M:%S");
		ssckey = SCKEY
		send_url = 'http://sctapi.ftqq.com/'+ SCKEY +'.send'
		if code == 0 and status!=1 :
			params = {
				'title': localtime+'bilibiliǩ���ɹ�',
				'desp': '����'+str(day_count)+'��ǩ��\n''��������'+str(points)+'��'
			}
		elif status == 1:
			params = {
				'title':  localtime+'bilibili�Ѿ�ǩ����',
				'desp': '����'+str(day_count)+'��ǩ��\n''��������'+str(points)+'��'
			}
		else:
			params = {
				'title':  localtime+'bilibiliǩ��ʧ��',
			}
		data = requests.post(send_url,headers=headers, data=params).content.decode()
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

	# pushWechat(code,status,day_count,points)
	bot = get_bot()
	if code == 0:
		msg='ǩ���ɹ�������'+str(day_count)+'��ǩ��\n''��������'+str(points)+'��'
	elif status == 1:
		msg='�Ѿ�ǩ��������'+str(day_count)+'��ǩ��\n''��������'+str(points)+'��'
	else:
		msg='ǩ��ʧ��,������cookiesʧЧ������������cookies'
	await bot.send_private_msg(user_id='1950655144', message=msg)
	return
	# #�Զ���Ʊ
	# locale.setlocale(locale.LC_CTYPE, 'chinese')
	#
	# while time.strftime('%H:%M') >= "12:00":
	# 	i = 0
	# 	while i<5 :
	# 		piaozi_list_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/ListProduct?device=h5&platform=web'
	#
	# 		piaozi_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/Exchange?device=h5&platform=web'
	#
	# 		piaozi_list_response = session.post(piaozi_list_url,headers=headers).content.decode()
	# 		data = json.loads(piaozi_list_response)['data'][0]
	# 		id = data['id']
	# 		cost = data['real_cost']
	#
	# 		piaozi_Body = {
	# 			'product_id': id,
	# 			'product_num': 1,
	# 			'point': cost
	# 		}
	# 		piaozi_data = session.post(piaozi_url,headers=headers,data=piaozi_Body).content.decode()
	# 		data = json.loads(piaozi_data)
	# 		msg = data['msg']
	# 		code = data['code']
	# 		print('�����С���������\n������Ϊ')
	# 		print(msg)
	# 		i=i+1
	# 		time.sleep(5)