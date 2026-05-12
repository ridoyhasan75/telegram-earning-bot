from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    keyboard = [
        [KeyboardButton(text="📋 Task"), KeyboardButton(text="👥 Referral")],
        [KeyboardButton(text="💰 Wallet"), KeyboardButton(text="🏧 Withdraw")],
        [KeyboardButton(text="ℹ️ Rules")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def cancel_menu():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True)
