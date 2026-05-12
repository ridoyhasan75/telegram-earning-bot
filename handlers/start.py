from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import database as db
from keyboards.reply import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    args = message.text.split()
    referred_by = None
    
    if len(args) > 1 and args[1].isdigit():
        ref_id = int(args[1])
        if ref_id != user_id:
            referred_by = ref_id

    await db.add_user(user_id, username, referred_by)
    
    user = await db.get_user(user_id)
    if user and user['is_banned']:
        await message.answer("❌ আপনি এই বট থেকে ব্যান হয়েছেন।")
        return

    welcome_text = (
        f"👋 স্বাগতম {username}!\n\n"
        "**টাকা ইনকাম বাংলাদেশ** বটে আপনাকে স্বাগতম। "
        "এখানে আপনি খুব সহজেই টাস্ক পূরণ করে এবং বন্ধুদের রেফার করে টাকা ইনকাম করতে পারবেন।\n\n"
        "নিচের মেনু থেকে আপনার অপশন সিলেক্ট করুন:"
    )
    
    await message.answer(welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@router.message(F.text == "❌ Cancel")
async def cmd_cancel(message: Message, state):
    await state.clear()
    await message.answer("❌ ক্যানসেল করা হয়েছে। মেনু থেকে অপশন বেছে নিন:", reply_markup=main_menu())

@router.message(F.text == "ℹ️ Rules")
async def cmd_rules(message: Message):
    rules = (
        "📜 **আমাদের নিয়মাবলী:**\n\n"
        "১. সব চ্যানেলে জয়েন থাকতে হবে, লিভ নিলে একাউন্ট ব্যান হবে।\n"
        "২. ফেক রেফার করলে পেমেন্ট পাবেন না এবং একাউন্ট ব্যান হবে।\n"
        "৩. রেফার করা বন্ধুকে অবশ্যই টাস্ক কমপ্লিট করতে হবে, নাহলে রেফার কাউন্ট হবে না।\n"
        "৪. পেমেন্ট রিকুয়েস্ট দেওয়ার ২৪-৪৮ ঘণ্টার মধ্যে পেমেন্ট ক্লিয়ার করা হবে।\n\n"
        "সততার সাথে কাজ করুন, ১০০% পেমেন্ট পাবেন!"
    )
    await message.answer(rules, parse_mode="Markdown")
