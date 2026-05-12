from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import database as db
from keyboards.inline import task_channels_menu
from utils.verification import check_membership

router = Router()

@router.message(F.text == "📋 Task")
async def show_task(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if user['is_banned']:
        return

    if user['tasks_completed']:
        await message.answer("✅ আপনি ইতিমধ্যেই টাস্ক সম্পূর্ণ করেছেন!")
        return

    settings = await db.get_settings()
    reward = settings['task_reward']

    text = (
        "📋 **টাস্ক কমপ্লিট করুন**\n\n"
        "নিচের চ্যানেল গুলোতে জয়েন করুন এবং '✅ Verify' বাটনে ক্লিক করুন। "
        f"সব চ্যানেল জয়েন করলে আপনি {reward} টাকা বোনাস পাবেন!"
    )
    
    await message.answer(text, reply_markup=task_channels_menu(), parse_mode="Markdown")

@router.callback_query(F.data == "verify_task")
async def verify_task_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    
    if user['tasks_completed']:
        await callback.answer("✅ আপনি ইতিমধ্যেই টাস্ক সম্পূর্ণ করেছেন!", show_alert=True)
        return

    is_member = await check_membership(callback.bot, user_id)
    
    if is_member:
        settings = await db.get_settings()
        reward = settings['task_reward']
        success = await db.complete_task(user_id, reward)
        
        if success:
            await callback.message.edit_text(f"🎉 অভিনন্দন! আপনি সফলভাবে সব চ্যানেল জয়েন করেছেন।\nআপনাকে {reward} টাকা বোনাস দেওয়া হয়েছে।")
        else:
            await callback.answer("কোথাও কোনো সমস্যা হয়েছে।", show_alert=True)
    else:
        await callback.answer("❌ আপনি এখনো সব চ্যানেলে জয়েন করেননি! সব চ্যানেলে জয়েন করে আবার চেষ্টা করুন।", show_alert=True)
