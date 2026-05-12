from aiogram import Router, F
from aiogram.types import Message
import database as db

router = Router()

@router.message(F.text == "👥 Referral")
async def show_referral(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if user['is_banned']:
        return

    bot_info = await message.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
    
    text = (
        "👥 **রেফারেল প্রোগ্রাম**\n\n"
        f"আপনার রেফারেল লিংক:\n`{ref_link}`\n\n"
        "আপনার লিংক দিয়ে কাউকে জয়েন করালে এবং সে টাস্ক কমপ্লিট করলে তা 'Valid Referral' হিসেবে গণ্য হবে।\n\n"
        f"Total Referrals: {user['total_referrals']}\n"
        f"Valid Referrals: {user['valid_referrals']}"
    )
    
    await message.answer(text, parse_mode="Markdown")
