from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import database as db
from keyboards.inline import withdraw_methods_menu
from keyboards.reply import cancel_menu, main_menu
from states.bot_states import WithdrawState
from config import ADMIN_ID

router = Router()

@router.message(F.text == "🏧 Withdraw")
async def cmd_withdraw(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    settings = await db.get_settings()
    
    if user['is_banned']:
        return

    if user['valid_referrals'] < 5:
        await message.answer(
            "❌ পেমেন্ট রিকোয়েস্ট দিতে আপনার কমপক্ষে ৫ টি ভ্যালিড রেফার লাগবে।\n"
            f"আপনার বর্তমান ভ্যালিড রেফার: {user['valid_referrals']}"
        )
        return
    elif user['valid_referrals'] >= 5 and user['valid_referrals'] < 15:
        remaining = 15 - user['valid_referrals']
        await message.answer(
            f"❌ পেমেন্ট রিকোয়েস্ট দিতে আপনার আরও {remaining} টি ভ্যালিড রেফার লাগবে।\n"
            f"আপনার বর্তমান ভ্যালিড রেফার: {user['valid_referrals']}"
        )
        return
        
    if user['balance'] <= 0:
        await message.answer("❌ আপনার ব্যালেন্স নেই।")
        return

    await message.answer("পেমেন্ট মেথড সিলেক্ট করুন:", reply_markup=withdraw_methods_menu())

@router.callback_query(F.data.startswith("withdraw_"))
async def process_withdraw_method(callback: CallbackQuery, state: FSMContext):
    method = callback.data.split("_")[1].capitalize()
    await state.update_data(method=method)
    
    await callback.message.delete()
    await callback.message.answer(
        f"আপনি {method} সিলেক্ট করেছেন।\nআপনার {method} নাম্বার দিন:",
        reply_markup=cancel_menu()
    )
    await state.set_state(WithdrawState.waiting_for_number)

@router.message(WithdrawState.waiting_for_number)
async def process_withdraw_number(message: Message, state: FSMContext):
    number = message.text
    if len(number) < 11 or not number.isdigit():
        await message.answer("❌ সঠিক নাম্বার দিন।")
        return
        
    await state.update_data(number=number)
    user = await db.get_user(message.from_user.id)
    
    await message.answer(
        f"আপনার বর্তমান ব্যালেন্স: {user['balance']} টাকা\n"
        "আপনি কত টাকা তুলতে চান? (ইংরেজিতে লিখুন)",
        reply_markup=cancel_menu()
    )
    await state.set_state(WithdrawState.waiting_for_amount)

@router.message(WithdrawState.waiting_for_amount)
async def process_withdraw_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ সঠিক এমাউন্ট দিন।")
        return
        
    amount = int(message.text)
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if amount < 50:
        await message.answer("❌ সর্বনিম্ন ৫০ টাকা তুলতে পারবেন।")
        return
        
    if amount > user['balance']:
        await message.answer("❌ আপনার এতো ব্যালেন্স নেই।")
        return
        
    data = await state.get_data()
    method = data['method']
    number = data['number']
    
    # Update balance and save request
    await db.update_user_balance(user_id, -amount)
    await db.add_withdraw_request(user_id, method, number, amount)
    
    # Notify Admin
    try:
        from keyboards.inline import withdraw_action_menu
        pending = await db.get_pending_withdrawals()
        if pending:
            last_req = pending[-1]
            req_id = last_req['id']
            admin_msg = (
                "🆕 **New Withdraw Request**\n\n"
                f"User ID: `{user_id}`\n"
                f"Method: {method}\n"
                f"Number: `{number}`\n"
                f"Amount: {amount} TK"
            )
            await message.bot.send_message(
                ADMIN_ID, 
                admin_msg, 
                reply_markup=withdraw_action_menu(req_id, user_id),
                parse_mode="Markdown"
            )
    except Exception as e:
        print(f"Error notifying admin: {e}")

    await state.clear()
    await message.answer("✅ আপনার পেমেন্ট রিকোয়েস্ট সফলভাবে এডমিনের কাছে পাঠানো হয়েছে।", reply_markup=main_menu())
