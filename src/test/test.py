import nonebot.adapters.onebot.v11.bot
from nonebot import on_keyword,on_command
import random
from datetime import date
from nonebot.adapters.onebot.v11 import message
from nonebot.adapters.onebot.v11 import Bot, Event

luck=on_keyword("luck",priority=1)
tome=on_keyword("tome",priority=1)

@luck.handle()
async def luck_res(bot:Bot,event:Event):
    rnd=random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    lucknum=rnd.randint(1,100)
    await luck.finish(message=f"今日的运气值是:{lucknum}")

@tome.handle()
async def tome_res(bot:Bot,event:Event):
    pass