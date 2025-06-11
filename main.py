
from operator import contains
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.api.event import MessageChain
from astrbot.core.platform import AstrMessageEvent
import astrbot.core.message.components as Comp
from astrbot.api import logger
from astrbot.core.platform.astr_message_event import MessageSesion # 使用 astrbot 提供的 logger 接口

@register("astrbot_plugin_pandown", "IMZCC", "获取 PanDown 加速链接", "1.0.0")
class PanDownPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("pandown", alias={""}, desc="获取 PanDown 加速链接")
    # @filter.platform_adapter_type(filter.PlatformAdapterType.VCHAT)
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def on_command(self, event: AstrMessageEvent):
        # event.should_call_llm(False)
        user_name = event.get_sender_name()
        logger.info("触发pandown指令!")
        message_chain = MessageChain().message("领取加速链接")
        message_session = MessageSesion.from_str("wechatpadpro:FriendMessage:gh_ace9856008e1")
        await self.context.send_message(message_session, message_chain)
        yield event.plain_result(f"pandown execute command")

    @filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
    async def on_message(self, event: AstrMessageEvent):
        # event.should_call_llm(False)
        if event.get_sender_id() != "gh_ace9856008e1":
            return
        if contains(event.get_message_str(), "您的加速链接"):
            logger.info(f"收到回复：{event.get_message_str}")
            message_chain = MessageChain().message(event.get_message_str())
            message_session = MessageSesion.from_str("wechatpadpro:FriendMessage:wxid_2bkjmmx2pddb21")
            logger.info(f"发送消息：{message_chain}")
            await self.context.send_message(message_session, message_chain)
        else:
            message_chain = MessageChain().message("我的加速链接")
            message_session = MessageSesion.from_str("wechatpadpro:FriendMessage:gh_ace9856008e1")
            logger.info(f"发送消息：{message_chain}")
            await self.context.send_message(message_session, message_chain)
        


