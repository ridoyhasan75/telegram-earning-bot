import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 0,
                total_referrals INTEGER DEFAULT 0,
                valid_referrals INTEGER DEFAULT 0,
                tasks_completed BOOLEAN DEFAULT 0,
                referred_by INTEGER DEFAULT NULL,
                is_banned BOOLEAN DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS withdrawals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                method TEXT,
                number TEXT,
                amount INTEGER,
                status TEXT DEFAULT 'pending'
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY DEFAULT 1,
                task_reward INTEGER DEFAULT 150,
                min_withdraw_referrals INTEGER DEFAULT 15
            )
        ''')
        await db.execute('INSERT OR IGNORE INTO settings (id, task_reward, min_withdraw_referrals) VALUES (1, 150, 15)')
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchone()

async def add_user(user_id, username, referred_by=None):
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute('INSERT INTO users (user_id, username, referred_by) VALUES (?, ?, ?)', (user_id, username, referred_by))
            if referred_by:
                await db.execute('UPDATE users SET total_referrals = total_referrals + 1 WHERE user_id = ?', (referred_by,))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False

async def update_user_balance(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def complete_task(user_id, reward):
    async with aiosqlite.connect(DB_NAME) as db:
        user = await get_user(user_id)
        if user and not user['tasks_completed']:
            await db.execute('UPDATE users SET tasks_completed = 1, balance = balance + ? WHERE user_id = ?', (reward, user_id))
            if user['referred_by']:
                await db.execute('UPDATE users SET valid_referrals = valid_referrals + 1 WHERE user_id = ?', (user['referred_by'],))
            await db.commit()
            return True
        return False

async def get_settings():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM settings WHERE id = 1') as cursor:
            return await cursor.fetchone()

async def add_withdraw_request(user_id, method, number, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO withdrawals (user_id, method, number, amount) VALUES (?, ?, ?, ?)', (user_id, method, number, amount))
        await db.commit()

async def get_withdraw_history(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM withdrawals WHERE user_id = ? ORDER BY id DESC LIMIT 5', (user_id,)) as cursor:
            return await cursor.fetchall()
            
async def get_all_users_count():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT COUNT(*) FROM users') as cursor:
            return (await cursor.fetchone())[0]

async def get_active_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT COUNT(*) FROM users WHERE is_banned = 0') as cursor:
            return (await cursor.fetchone())[0]

async def get_completed_tasks_count():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT COUNT(*) FROM users WHERE tasks_completed = 1') as cursor:
            return (await cursor.fetchone())[0]

async def get_pending_withdrawals():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM withdrawals WHERE status = "pending"') as cursor:
            return await cursor.fetchall()

async def update_withdraw_status(withdraw_id, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE withdrawals SET status = ? WHERE id = ?', (status, withdraw_id))
        await db.commit()

async def ban_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
        await db.commit()

async def unban_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
        await db.commit()

async def update_settings(task_reward=None, min_withdraw_referrals=None):
    async with aiosqlite.connect(DB_NAME) as db:
        if task_reward is not None:
            await db.execute('UPDATE settings SET task_reward = ? WHERE id = 1', (task_reward,))
        if min_withdraw_referrals is not None:
            await db.execute('UPDATE settings SET min_withdraw_referrals = ? WHERE id = 1', (min_withdraw_referrals,))
        await db.commit()

async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT user_id FROM users WHERE is_banned = 0') as cursor:
            return await cursor.fetchall()
