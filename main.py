import os
import time
import threading


# --- Function to show macOS notification ---
def show_notification(msg):
    os.system(f'''osascript -e 'display notification "{msg}" with title "Reminder"' ''')


# --- Convert all time units to seconds ---
def convert_to_seconds(seconds=0, minutes=0, hours=0, days=0, weeks=0):
    return seconds + minutes*60 + hours*3600 + days*86400 + weeks*604800


# --- Function to handle a reminder ---
def set_reminder(message, delay_seconds):
    print(f"⏰ Reminder set: '{message}' (will trigger in {delay_seconds} seconds)")
    time.sleep(delay_seconds)
    show_notification(message)
    print(f"✅ Reminder shown: '{message}'")


# --- MAIN PROGRAM ---
if __name__ == "__main__":
    reminders = []
    print("📋 Reminder Setup — type 'done' when finished.\n")

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
            print("⚠️ Please enter valid numbers for time.")
            continue

        delay = convert_to_seconds(seconds, minutes, hours, days, weeks)
        if delay <= 0:
            print("⚠️ Time must be greater than zero.")
            continue

        reminders.append({"message": msg, "time": delay})
        print(f"✅ Reminder '{msg}' scheduled!\n")

    if not reminders:
        print("No reminders set. Exiting.")
        exit()

    print(f"\n🕐 Starting {len(reminders)} reminder(s)...\n")

    # Run reminders concurrently
    threads = []
    for r in reminders:
        t = threading.Thread(target=set_reminder, args=(r["message"], r["time"]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n🎉 All reminders completed!")
