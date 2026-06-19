# Sakai UG Telegram Bot

Get notified on Telegram for new announcements, assignments, grades, and messages from sakai.ug.edu.gh — every 15 minutes.

---

## Setup

### 1. Install Python
Download from https://python.org (version 3.8+)

### 2. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Create your Telegram Bot
1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **bot token** it gives you

### 4. Get your Telegram Chat ID
1. Search for **@userinfobot** on Telegram
2. Send it any message
3. It will reply with your **Chat ID**

### 5. Configure your credentials
Copy `.env.example` to `.env` and fill in your details:
```
SAKAI_USERNAME=your_student_id
SAKAI_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=123456:ABCdef...
TELEGRAM_CHAT_ID=123456789
```

### 6. Run the bot
```bash
python main.py
```

---

## Deploy to Render (24/7)

1. Push this folder to a **GitHub repo**
2. Go to https://render.com and create a free account
3. Click **New → Web Service** → connect your repo
4. Set:
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium && playwright install-deps`
   - **Start Command**: `python main.py`
5. Add your environment variables (from `.env`) under **Environment**
6. Click **Deploy**

That's it — the bot runs 24/7 for free!

---

## What it monitors
- 📢 Announcements
- 📝 Assignments (with due dates)
- 📊 Grades
- ✉️ Messages
