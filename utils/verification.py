from aiogram import Bot
from config import CHANNELS

async def check_membership(bot: Bot, user_id: int) -> bool:
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            # Assume false if we can't verify
            return False
    return True
