from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS

def task_channels_menu():
    keyboard = []
    for i, channel in enumerate(CHANNELS, 1):
        keyboard.append([InlineKeyboardButton(text=f"Join Channel {i}", url=f"https://t.me/{channel.replace('@', '')}")])
    keyboard.append([InlineKeyboardButton(text="✅ Verify", callback_data="verify_task")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def withdraw_methods_menu():
    keyboard = [
        [InlineKeyboardButton(text="bKash", callback_data="withdraw_bkash"),
         InlineKeyboardButton(text="Nagad", callback_data="withdraw_nagad")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def admin_panel_menu():
    keyboard = [
        [InlineKeyboardButton(text="📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton(text="💸 Pending Withdraws", callback_data="admin_withdraws")],
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="⚙️ Settings", callback_data="admin_settings")],
        [InlineKeyboardButton(text="🚫 Ban User", callback_data="admin_ban"),
         InlineKeyboardButton(text="✅ Unban User", callback_data="admin_unban")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def withdraw_action_menu(withdraw_id, user_id):
    keyboard = [
        [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve_{withdraw_id}_{user_id}"),
         InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_{withdraw_id}_{user_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
