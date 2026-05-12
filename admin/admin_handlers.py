from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import database as db
from config import ADMIN_ID
from keyboards.inline import admin_panel_menu
from keyboards.reply import cancel_menu, main_menu
from states.bot_states import AdminState
import asyncio

router = Router()

def is_admin(user_id):
    return user_id == ADMIN_ID

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("👨‍💻 **Admin Panel**", reply_markup=admin_panel_menu(), parse_mode="Markdown")

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    total = await db.get_all_users_count()
    active = await db.get_active_users()
    tasks = await db.get_completed_tasks_count()
    
    text = (
        "📊 **Bot Statistics**\n\n"
        f"Total Users: {total}\n"
        f"Active Users: {active}\n"
        f"Completed Tasks: {tasks}"
    )
    await callback.message.edit_text(text, reply_markup=admin_panel_menu(), parse_mode="Markdown")

@router.callback_query(F.data == "admin_withdraws")
async def admin_withdraws(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
        
    pending = await db.get_pending_withdrawals()
    if not pending:
        await callback.answer("No pending withdrawals.", show_alert=True)
        return
        
    await callback.message.delete()
    for req in pending:
        from keyboards.inline import withdraw_action_menu
        text = (
            "💸 **Pending Request**\n\n"
            f"ID: {req['id']}\n"
            f"User ID: `{req['user_id']}`\n"
            f"Method: {req['method']}\n"
            f"Number: `{req['number']}`\n"
            f"Amount: {req['amount']} TK"
        )
        await callback.message.answer(text, reply_markup=withdraw_action_menu(req['id'], req['user_id']), parse_mode="Markdown")

@router.callback_query(F.data.startswith("approve_"))
async def approve_withdraw(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
        
    data = callback.data.split("_")
    req_id = int(data[1])
    user_id = int(data[2])
    
    await db.update_withdraw_status(req_id, "approved")
    await callback.message.edit_text(callback.message.text + "\n\n✅ **APPROVED**")
    
    try:
        await callback.bot.send_message(user_id, "🎉 আপনার পেমেন্ট রিকোয়েস্ট অ্যাপ্রুভ করা হয়েছে! টাকা আপনার একাউন্টে পাঠিয়ে দেওয়া হয়েছে।")
    except:
        pass

@router.callback_query(F.data.startswith("reject_"))
async def reject_withdraw(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
        
    data = callback.data.split("_")
    req_id = int(data[1])
    user_id = int(data[2])
    
    await db.update_withdraw_status(req_id, "rejected")
    await callback.message.edit_text(callback.message.text + "\n\n❌ **REJECTED**")
    
    try:
        await callback.bot.send_message(user_id, "❌ আপনার পেমেন্ট রিকোয়েস্ট রিজেক্ট করা হয়েছে। কোনো ভুলের কারণে এটি হতে পারে।")
    except:
        pass

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.message.answer("Enter the message to broadcast to all users:", reply_markup=cancel_menu())
    await state.set_state(AdminState.waiting_for_broadcast)

@router.message(AdminState.waiting_for_broadcast)
async def process_broadcast(message: Message, state: FSMContext):
    users = await db.get_all_users()
    await state.clear()
    await message.answer(f"Starting broadcast to {len(users)} users...", reply_markup=main_menu())
    
    success = 0
    for user in users:
        try:
            await message.send_copy(chat_id=user[0])
            success += 1
            await asyncio.sleep(0.05)
        except:
            pass
            
    await message.answer(f"Broadcast completed! Sent to {success} users.")

@router.callback_query(F.data == "admin_ban")
async def admin_ban_prompt(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.message.answer("Enter User ID to Ban:", reply_markup=cancel_menu())
    await state.set_state(AdminState.waiting_for_ban_id)

@router.message(AdminState.waiting_for_ban_id)
async def process_ban(message: Message, state: FSMContext):
    if message.text.isdigit():
        await db.ban_user(int(message.text))
        await message.answer("User banned successfully.", reply_markup=main_menu())
    else:
        await message.answer("Invalid ID.")
    await state.clear()

@router.callback_query(F.data == "admin_unban")
async def admin_unban_prompt(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.message.answer("Enter User ID to Unban:", reply_markup=cancel_menu())
    await state.set_state(AdminState.waiting_for_unban_id)

@router.message(AdminState.waiting_for_unban_id)
async def process_unban(message: Message, state: FSMContext):
    if message.text.isdigit():
        await db.unban_user(int(message.text))
        await message.answer("User unbanned successfully.", reply_markup=main_menu())
    else:
        await message.answer("Invalid ID.")
    await state.clear()

@router.callback_query(F.data == "admin_settings")
async def admin_settings(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    settings = await db.get_settings()
    text = (
        "⚙️ **Settings**\n\n"
        f"Task Reward: {settings['task_reward']} TK\n"
        f"Min Withdraw Referrals: {settings['min_withdraw_referrals']}\n\n"
        "Send new Task Reward amount (or /cancel to abort):"
    )
    await callback.message.edit_text(text, parse_mode="Markdown")
    await state.set_state(AdminState.waiting_for_reward_amount)

@router.message(AdminState.waiting_for_reward_amount)
async def process_reward_amount(message: Message, state: FSMContext):
    if message.text == '/cancel':
        await state.clear()
        return
    if message.text.isdigit():
        await db.update_settings(task_reward=int(message.text))
        await message.answer("Send new Minimum Withdraw Referrals requirement:")
        await state.set_state(AdminState.waiting_for_ref_req)
    else:
        await message.answer("Invalid amount.")

@router.message(AdminState.waiting_for_ref_req)
async def process_ref_req(message: Message, state: FSMContext):
    if message.text.isdigit():
        await db.update_settings(min_withdraw_referrals=int(message.text))
        await message.answer("Settings updated successfully!")
    else:
        await message.answer("Invalid amount.")
    await state.clear()
