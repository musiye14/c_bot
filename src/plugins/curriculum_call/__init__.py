import json
import os
import time

import pandas as pd
import json
import re
from datetime import datetime
from nonebot import require, on_keyword, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message,MessageSegment
from nonebot.rule import to_me
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot import get_bot

filename = 'src/plugins/curriculum_call/class_data.json'
def save(data):
    with open("src/plugins/curriculum_call/class_data.json", "w") as f:
        json.dump(data,f)

if not os.path.exists(filename):
    class_data={'':[""]}
    save(class_data)



day_time = ["1-2", "3-4", "5-6", "7-8", "9-11"]
real_day_time = {"1-2": "教一  8:20-9:55 教二 8:30-10:05",
                 "3-4": "教一  10:15-11:50 教二 10:35-12:10",
                 "5-6": "教一教二  13:30-15:05 ",
                 "7-8": "教一教二  15:15-16:50 ",
                 "9-11": "教一教二  18:30-20:55 "
                 }
# 每分钟检测一次直到检测到   提醒时间 就提醒
time_transport = ["8:05", "10:00", "13:10", "15:05", "18:10"]

scheduler = require("nonebot_plugin_apscheduler").scheduler
sheet_name = '课表'

table = pd.read_excel('src/plugins/curriculum_call/curriculum.xls', sheet_name=sheet_name)

called = on_command("课程提醒", rule=to_me(), aliases={"课程", "课程通知", "课程提醒"}, priority=20)
called_del = on_command("删除课程提醒", rule=to_me(), aliases={"取消课程提醒","取消提醒","删除班级","关闭提醒"}, priority=20)
curr_today = on_keyword(["今天课程","今天上什么","明天上什么","明天课程","今日课程","明日课程"],rule=to_me(),priority=20)

# called.expire_time

def look():
    with open("src/plugins/curriculum_call/class_data.json", "r") as f:
        data = json.load(f)
        # print("加载完成：")
        # print(data)
    return data


def save_qq(data):
    with open("src/plugins/curriculum_call/class_data.json", "w") as f:
        json.dump(data, f)


# 增加函数
def add_qq(class_id, qq_id):
    del_qq(qq_id)
    class_data = look()
    if (class_id not in class_data):
        class_data[class_id] = [qq_id]
    else:
        class_data[class_id].append(qq_id)
    save_qq(class_data)
    # print("增加后：")
    # print(class_data)


# 删除函数
def del_qq(qq_id):
    class_data = look()
    for i in class_data:
        if (class_data[i].count(qq_id) != 0):
            class_data[i].remove(qq_id)
    save_qq(class_data)
    # print("删除后：")
    # print(class_data)


# 找同一个班级的qq号
def find_qqs(class_id):
    class_data = look()
    qqs = class_data[class_id]
    return qqs

def find_class(qq_id):
    class_data = look()
    #顺序遍历  可以考虑之后用二分之类的
    for i in class_data:
        if (class_data[i].count(qq_id)!= 0):
            return i

# 取消提醒功能
@called_del.handle()
async def ca_del(event:Event):
    del_qq(event.get_user_id())
    await called_del.send("关闭提醒功能")
    return

# 保存班级信息
@called.handle()
async def update(bot: Bot, event: Event, args: Message = CommandArg(), matcher=Matcher):
    plain_text = args.extract_plain_text()
    if plain_text and plain_text[0] == 'B' and plain_text[1:-1].isdigit():
        matcher.set_arg("c", args)

# 检查班级信息是否合格
@called.got("c", prompt="请输入班级信息 注意B要大写 超过2分钟就要重新输入哦 需要更改班级就重新输入指令")
async def class_run(bot: Bot, event: Event, c: Message = Arg(), class_id: str = ArgPlainText("c")):
    raw=event.get_message()
    print(raw)
    print([raw])
    if("CQ:" in raw):
        print("不是汉字")
        return
    if(not MessageSegment.is_text):
        print("不是文字")
        return
    if (class_id == "1"):
        return
    column_name = table.columns.values
    for index, i in enumerate(column_name):
        i = str(i)
        class_name = column_name[index]
        t = i.find(class_id)
        if (t != -1):
            break

    if (t == -1):
        await called.reject_arg("c", "没有找到班级 注意格式（B要大写）请重新输入")
    if(class_id==""):

        return
    # 班级号正确之后
    qq_id = event.get_user_id()
    add_qq(class_id, qq_id)
    await called.send("成功开启提醒功能")
    return


    # 命令的执行程序
    # 检测一下是否有定时任务在列表里  有的话删除后重新添加
# time_transport = ["8:05", "10:00", "13:10", "15:05", "11:50"]
for tt in time_transport:
    hour = tt.split(":")[0]
    minute = tt.split(":")[1]
    task_id = hour + ":" + minute
    l = scheduler.get_job(task_id)
    if (l != None):
        scheduler.remove_job(job_id=task_id)
        print(f"删除了任务{task_id}")

    # 测试
    # hour=datetime.now().hour
    # minute=datetime.now().minute
    print(str(hour) + ":" + str(minute))

    # 根据qq号与提醒时间设定任务


    @scheduler.scheduled_job('cron', hour=hour, minute=minute, id=task_id)
    # @scheduler.scheduled_job('interval',minutes=1, id=task_id)
    async def call_class():

        column_name = table.columns.values
        column_week_name = table.columns.values[0]
        column_course_name = table.columns.values[1]
        t = datetime.now()
        if (t.minute < 10 and t.hour<10):
            true_time = f"0{t.hour}:0{t.minute}"
        elif(t.minute < 10):
            true_time = f"{t.hour}:0{t.minute}"
        elif(t.hour <10):
            true_time = f"0{t.hour}:{t.minute}"
        else:
            true_time = f"{t.hour}:{t.minute}"
        # print(hour,minute)

        print(true_time)
        # "8:05","10:00","13:10","15:05","18:10" 下面用来减少误差
        if (true_time >= "08:00" and true_time <= "08:20"):
            true_time = time_transport[0]
        elif (true_time >= "09:55" and true_time <= "10:15"):
            true_time = time_transport[1]
        elif (true_time >= "13:05" and true_time <= "13:30"):
            true_time = time_transport[2]

        elif (true_time >= "15:00" and true_time <= "15:15"):
            true_time = time_transport[3]
        elif (true_time >= "18:20" and true_time <= "18:40"):
            true_time = time_transport[4]
        print(true_time)
        #第几节课
        transport_time = time_transport.index(true_time)
        # print(transport_time)

        # 把2022/2/28看做是第一周
        old = datetime(2022, 2, 28)
        now = datetime.now()
        count = (now - old).days

        class_name = ""
        # 获取今天是第几周
        week = int(count / 7 + 1)
        # 判今天是星期几 0-4表示周一 到周五
        day = str(datetime.now().weekday())

        data = look()
        # 拿取对应班级
        for c_i in data:
            if(c_i==""):
                continue
            class_id=c_i
            #找到一个班里的qq号
            qqs=find_qqs(class_id)
            if(not qqs):
                continue

            for index, i in enumerate(column_name):
                i = str(i)
                # 取每一个列名
                class_name = column_name[index]
                # 查找这个列名是否包含这个班级名
                t = i.find(class_id)
                if (t != -1):
                    break;
            if (class_name == ""):
                print("没有找到对应班级")
            else:
                new_table = table[[column_course_name, class_name]]



            # 把特殊的实习信息拿出来
            special_days = new_table.iloc[0]
            # 初始化一下 把课程的信息放到对应的天里去  weeks 0-4对应周一到周五
            weeks = {}
            # 按星期为单位取课   1-5周一  6-10周二  11-15周三 16-20周四  21-25周五 一天5个课时分段 step=5
            for index, i in enumerate(range(1, 26, 5)):
                # print(new_table.loc[i:i+4].values)
                line = new_table.loc[i:i + 4].values
                name = {}
                # j表示每天的每个时段的课
                for j in line:
                    name[j[0]] = j[1]
                weeks[str(index)] = name

            # print(weeks['0']["3-4"].split('\n'))
            # 从对应的天中取出当天的所有课程
            # print(weeks)
            # 选取时段
            # for x in datetime:
            # 提取 星期day 时刻 day_time的课程
            curriculums = weeks[day][day_time[transport_time]]
            if (pd.isna(curriculums)):
                print(day_time[transport_time] + "没课")
                return
            curriculums = curriculums.split('\n')


            # 遍历所有在那天的那个时段的可能课程
            for i in curriculums:

                # i=i.replace(" ","")
                course = i
                i = i.replace(" ", "")
                cheak = i[-1:-4:-1]
                cheak = cheak.isdigit() or cheak.isalpha()

                # cheak的状态 表示 两种课程类型  false= 大学体育IIII 3-8，10，12-16    ture= 大学英语IV 1-10,12-15 杨曦 语音室A 或者  数字电子技术课程设计16周 白燕燕 实408
                # 根据cheak 的状态选择不同的匹配方式
                if (cheak == True):
                    pat = re.compile(r'(?<=\D)\d\d?-\d\d?(?=\D)|\d\d?(?=周)')
                    dt = pat.findall(i)
                    # print(dt)
                else:
                    pat = re.compile(r'(?=[\w]*)\d\d?-\d\d?(?=[\w]*)|(?=\w*)\d\d?(?=\w*)')
                    dt = pat.findall(i)
                    # print(dt)

                for t in dt:
                    # print(t)
                    class_choose = t.split("，")
                    if (len(class_choose) == 1):
                        class_choose = class_choose[0].split(",")
                    """可能的形式有   1-10，13-15，17  ----->    [1-10  ,13-15  ,17 ]------>  [1,10] """

                    for j in class_choose:
                        c = j.split("-")
                        # print(len(c)) #5
                        # print(c)
                        bot=get_bot()
                        if (len(c) > 1):
                            if (week >= int(c[0]) and week <= int(c[1])):
                                for qq in qqs:
                                    msg=course + "\n" + "上课时间：" + real_day_time[day_time[transport_time]]
                                    await bot.send_private_msg(user_id=qq, message=msg)
                                    # print(course)
                                    # print(real_day_time[day_time[transport_time]])
                        else:
                            if (week == int(c[0])):
                                for qq in qqs:
                                    msg = course + "\n" + "上课时间：" + real_day_time[day_time[transport_time]]
                                    await bot.send_private_msg(user_id=qq, message=msg)
                                    # print(course)
                                    # print(real_day_time[day_time[transport_time]])
        return



@curr_today.handle()
async  def wacth(bot:Bot,event:Event):
    content=event.get_message()
    # 如果有明天或者明日就天数加一
    content=content.count("明天")+content.count("明日")
    old = datetime(2022, 2, 28)
    now = datetime.now()
    count = (now - old).days
    # 获取今天是第几周
    week = int(count / 7 + 1)
    # 判今天是星期几 0-4表示周一 到周五
    day = str(datetime.now().weekday()+content)
    if(day>4):
        # 今天是周末
        curr_today.send("今天是周末")
        return
    sheet_name = '课表'
    time_transport = ["8:05", "10:00", "13:10", "15:05", "18:10"]
    table = pd.read_excel('D:\p_projects\\robot\c_bot\src\plugins\curriculum_call\curriculum.xls',
                          sheet_name=sheet_name)
    t = datetime.now()
    column_course_name = table.columns.values[1]
    class_id = find_class("1950655144")
    day_time = ["1-2", "3-4", "5-6", "7-8", "9-11"]
    real_day_time = {"1-2": "教一  8:20-9:55 教二 8:30-10:05",
                     "3-4": "教一  10:15-11:50 教二 10:35-12:10",
                     "5-6": "教一教二  13:30-15:05 ",
                     "7-8": "教一教二  15:15-16:50 ",
                     "9-11": "教一教二  18:30-20:55 "
                     }
    # 每分钟检测一次直到检测到   提醒时间 就提醒
    time_transport = ["8:05", "10:00", "13:10", "15:05", "18:10"]

    # 班级名列表
    column_name = table.columns.values
    if (not class_id):
        print("找不到你的班级")
        # return
    for index, i in enumerate(column_name):
        i = str(i)
        class_name = column_name[index]
        t = i.find(class_id)
        if (t != -1):
            break;
    if (class_name == ""):
        print("没有找到对应班级")
    else:
        new_table = table[[column_course_name, class_name]]
    weeks = {}
    for index, i in enumerate(range(1, 26, 5)):
        # print(new_table.loc[i:i+4].values)
        line = new_table.loc[i:i + 4].values
        name = {}
        for j in line:
            name[j[0]] = j[1]
        weeks[str(index)] = name


    curriculums = weeks[day]

    # h 和ww 只是用来转换一下  最后i会取到一天的每一节课
    for index, h in enumerate(curriculums):
        ww = curriculums[h]

        if (pd.isna(ww)):
            break
        transport_time = index
        for i in ww.split('\n'):
            # i=i.replace(" ","")
            course = i
            i = i.replace(" ", "")
            cheak = i[-1:-4:-1]
            cheak = cheak.isdigit() or cheak.isalpha()

            # cheak的状态 表示 两种课程类型  false= 大学体育IIII 3-8，10，12-16    ture= 大学英语IV 1-10,12-15 杨曦 语音室A 或者  数字电子技术课程设计16周 白燕燕 实408
            # 根据cheak 的状态选择不同的匹配方式
            if (cheak == True):
                pat = re.compile(r'(?<=\D)\d\d?-\d\d?(?=\D)|\d\d?(?=周)')
                dt = pat.findall(i)
                # print(dt)
            else:
                pat = re.compile(r'(?=[\w]*)\d\d?-\d\d?(?=[\w]*)|(?=\w*)\d\d?(?=\w*)')
                dt = pat.findall(i)
            # print(dt)
            for t in dt:
                # print(t)
                class_choose = t.split("，")
                if (len(class_choose) == 1):
                    class_choose = class_choose[0].split(",")
                """可能的形式有   1-10，13-15，17  ----->    [1-10  ,13-15  ,17 ]------>  [1,10] """
            for j in class_choose:
                # print(j)
                c = j.split("-")
                # bot = get_bot()
                # print(j)
                if (len(c) > 1):
                    if (week >= int(c[0]) and week <= int(c[1])):
                        msg = day_time[transport_time] + "节:  " + course
                        await curr_today.send(msg)
                        # print(day_time[transport_time] + "节:  " + course)
                else:
                    if (week == int(c[0])):
                        msg = day_time[transport_time] + "节:  " + course
                        await curr_today.send(msg)

    return