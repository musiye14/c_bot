import nonebot
from nonebot import on_command, on_request, on_notice, get_driver
from nonebot.adapters.onebot.v11 import MessageSegment, Message, FriendRequestEvent, GroupRequestEvent, Bot
from nonebot.rule import keyword, startswith, to_me
from nonebot.typing import T_State
from typing import Union


request_cmd = on_request(
    priority=14,
    block=True,
)


@request_cmd.handle()
async def handle_request(bot: Bot, event: Union[GroupRequestEvent, FriendRequestEvent], state: T_State):
    print(event.group_id)
    print("加群消息："+GroupRequestEvent.group_id)
    print("好友消息:"+FriendRequestEvent.get_user_id)
    print("是不是好友申请:"+isinstance(event,FriendRequestEvent))
    if isinstance(event, GroupRequestEvent):
        print("收到入群请求")
        await bot.set_group_add_request(
            flag=event.flag,
            sub_type=event.sub_type,
            approve=True,
            reason=""
        )
        nonebot.logger.info("同意加入群聊: {}", event. group_id)
        print("入群成功")
    elif isinstance(event, FriendRequestEvent):
        print("收到好友请求")
        await bot.set_friend_add_request(
            flag=event.flag,
            approve=True,
            remark=""
        )
        nonebot.logger.info("同意添加好友: {}", event.user_id)
        print("同意好友请求")