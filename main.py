import time
import schedule
from dotenv import load_dotenv
from sakai import get_data
from telegram_bot import send_message
from state import load_state, save_state, get_new_items, update_state

load_dotenv()

CHECK_INTERVAL_MINUTES = 15

EMOJI = {
    "announcements": "📢",
    "assignments": "📝",
    "grades": "📊",
    "messages": "✉️"
}

LABELS = {
    "announcements": "New Announcement",
    "assignments": "New Assignment",
    "grades": "New Grade Posted",
    "messages": "New Message"
}

def check_sakai():
    print(f"\n[Bot] Checking Sakai...")
    
    data = get_data()
    if data is None:
        send_message("⚠️ <b>Sakai Bot</b>: Could not log in. Please check your credentials.")
        return

    state = load_state()
    any_new = False

    for category in ["announcements", "assignments", "grades", "messages"]:
        items = data.get(category, [])
        new_items = get_new_items(category, items, state)

        if new_items:
            any_new = True
            emoji = EMOJI[category]
            label = LABELS[category]
            for item in new_items:
                msg = f"{emoji} <b>{label}</b>\n\n{item}"
                send_message(msg)
                print(f"[Bot] Sent: {item[:60]}...")

            state = update_state(category, items, state)

    if not any_new:
        print("[Bot] No new updates found.")

    save_state(state)

def main():
    print("=" * 40)
    print("  Sakai Telegram Bot Starting...")
    print(f"  Checking every {CHECK_INTERVAL_MINUTES} minutes")
    print("=" * 40)

    send_message("✅ <b>Sakai Bot is now running!</b>\nI'll notify you of new announcements, assignments, grades, and messages every 15 minutes.")

    # Run immediately on start
    check_sakai()

    # Then schedule every 15 minutes
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(check_sakai)

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    main()
