from aiogram.fsm.state import State, StatesGroup

class WithdrawState(StatesGroup):
    waiting_for_method = State()
    waiting_for_number = State()
    waiting_for_amount = State()

class AdminState(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_ban_id = State()
    waiting_for_unban_id = State()
    waiting_for_reward_amount = State()
    waiting_for_ref_req = State()
