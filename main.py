
from operator import contains
import time
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.api.event import MessageChain
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.platform import AstrMessageEvent
import astrbot.core.message.components as Comp
from astrbot.api import logger
from astrbot.core.platform.astr_message_event import MessageSesion # 使用 astrbot 提供的 logger 接口


@register("astrbot_plugin_pandown", "IMZCC", "获取 PanDown 加速链接", "1.0.0")
class PanDownPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.gh_id = self.config.get('gh_id')
        self.pending_requests = None

    @filter.command("pandown", alias={""}, desc="获取 PanDown 加速链接")
    @filter.permission_type(filter.PermissionType.ADMIN)
    async def on_command(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        user_id = event.get_sender_id()
        
        # 保存原始用户的会话信息
        self.pending_requests = event.unified_msg_origin
        
        logger.info(f"用户 {user_name} 触发pandown指令!")
        message_chain = MessageChain().message("领取加速链接")
        message_session = MessageSesion.from_str(self.gh_id)
        yield event.plain_result(f"正在为您获取加速链接，请稍候...")
        await self.context.send_message(message_session, message_chain)

    @filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE | filter.EventMessageType.GROUP_MESSAGE)
    async def on_message(self, event: AstrMessageEvent):
        if event.get_sender_id() != self.gh_id.split(":")[2]:
            return
        
        if contains(event.get_message_str(), "加速链接"):
            if contains(event.get_message_str(), "您的加速链接"):
                logger.info(f"收到回复：{event.get_message_str()}")
                
                # 发送给所有等待的用户
                message_chain = MessageChain().message(event.get_message_str())
                await self.context.send_message(self.pending_requests, message_chain)
                logger.info(f"已发送加速链接给用户 {self.pending_requests}")
            else:
                message_chain = MessageChain().message("我的加速链接")
                message_session = MessageSesion.from_str(self.gh_id)
                await self.context.send_message(message_session, message_chain)