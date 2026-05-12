# Taka Income BD Telegram Bot 🚀

A complete, production-ready Telegram earning bot built with Python 3, Aiogram 3.x, and aiosqlite. 
Users can earn balance by completing channel joining tasks, referring friends, and requesting withdrawals via bKash or Nagad.

## Features ✨
- **Async & Fast**: Built using the latest Aiogram framework.
- **Task System**: Auto-verifies channel membership.
- **Referral System**: Unique referral links, prevents self-referrals, requires referred users to complete tasks to count as valid.
- **Withdrawal System**: Minimum referral requirements, integrates bKash/Nagad.
- **Admin Panel**: Full control over users, broadcasts, banning, withdrawals, and dynamic settings.
- **Database**: Async SQLite handling.
- **Deployment Ready**: Fully structured for Replit, Render, Railway.

## Setup ⚙️

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file from `.env.example` and set your `BOT_TOKEN` and `ADMIN_ID`.
   ```env
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=your_telegram_id
   ```

3. **Run the bot**:
   ```bash
   python main.py
   ```

## Admin Commands 👨‍💻
- `/admin` - Opens the Admin Panel.

*Note: The bot needs to be added as an Admin in the verification channels to properly check membership status.*
