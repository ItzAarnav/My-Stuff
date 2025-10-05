import os
import time
import threading

"""
For this version, please make sure you have installed the 'notify-send' package!!!
"""

def show_notification(message, title="Reminder"):
    os.system(f'''notify-send "{title}" "{message}"''')

def convert_to_seconds(seconds=0, minutes=0, hours=0, days=0, weeks=0):
    return seconds + minutes*60 + hours*3600 + days*86400 + weeks*604800

def set_reminder(message, delay):
    print(f"⏰ Reminder set: '{message}' (in {delay} seconds)")
    time.sleep(delay)
    show_notification(message)
    print(f"✅ Reminder shown: '{message}'")

if __name__ == "__main__":
    reminders = []
    print("📋 Linux Reminder Setup — type 'done' when finished.\n")

    while True:
        msg = input("Enter reminder message (or 'done' to finish): ").strip()
        if msg.lower() == "done":
            break

        try:
            seconds = float(input("  Seconds: ") or 0)
            minutes = float(input("  Minutes: ") or 0)
            hours = float(input("  Hours: ") or 0)
            days = float(input("  Days: ") or 0)
            weeks = float(input("  Weeks: ") or 0)
        except ValueError:
            print("⚠️ Invalid number.")
            continue

        delay = convert_to_seconds(seconds, minutes, hours, days, weeks)
        if delay <= 0:
            print("⚠️ Time must be greater than zero.")
            continue

        reminders.append({"message": msg, "time": delay})
        print(f"✅ Reminder '{msg}' scheduled!\n")

    print(f"\n🕐 Starting {len(reminders)} reminder(s)...\n")

    threads = []
    for r in reminders:
        t = threading.Thread(target=set_reminder, args=(r["message"], r["time"]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n🎉 All reminders completed!")
