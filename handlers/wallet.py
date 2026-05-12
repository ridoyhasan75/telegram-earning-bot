from aiogram import Router, F
from aiogram.types import Message
import database as db

router = Router()

@router.message(F.text == "💰 Wallet")
async def show_wallet(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if user['is_banned']:
        return

    history = await db.get_withdraw_history(user_id)
    history_text = "\n".join([f"🔸 {h['amount']} TK ({h['method']}) - {h['status'].capitalize()}" for h in history])
    if not history_text:
        history_text = "কোনো রেকর্ড নেই"

    text = (
        "💰 **আপনার ওয়ালেট**\n\n"
        f"💵 বর্তমান ব্যালেন্স: {user['balance']} টাকা\n"
        f"👥 মোট রেফার: {user['total_referrals']}\n"
        f"✅ ভ্যালিড রেফার: {user['valid_referrals']}\n"
        f"📋 টাস্ক কমপ্লিট: {'হ্যাঁ' if user['tasks_completed'] else 'না'}\n\n"
        "📜 **উত্তোলনের হিস্ট্রি:**\n"
        f"{history_text}"
    )
    
    await message.answer(text, parse_mode="Markdown")
