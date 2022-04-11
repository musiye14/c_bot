import nonebot
from fastapi import FastAPI
from pydantic import BaseModel
from nonebot import get_bot
from nonebot.plugin import require
app: FastAPI = nonebot.get_app()

scheduler = require("nonebot_plugin_apscheduler").scheduler


"""设定了post接受的格式  =None表示可选可不选"""
class Item(BaseModel):
    message:str
    id:int
    time: str =None

"""设定了接口地址"""
@app.post("/say")

async def custom_api(item:Item):
    time=item.time
    id = item.id
    msg = item.message
    bot = get_bot()
    if(time==None):
        id = item.id
        msg = item.message
        await bot.send_private_msg(user_id=id,message=msg)
        return
    else:
        hour = time.split(":")[0]
        minute = time.split(":")[1]

        # @scheduler.scheduled_job('cron',second=9,id='say')
        @scheduler.scheduled_job('cron',hour=hour,minute=minute, id='say')
        async def time_say():

            scheduler.remove_job('say')
            bot = get_bot()
            await bot.send_private_msg(user_id=id, message=msg)
            return
        """记录一下定时发送时间"""