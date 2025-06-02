import tkinter as tk
from email.message import EmailMessage
import smtplib
import requests
import sqlite3
from datetime import datetime

# ========= ডাটাবেসে লগ করার ফাংশন =========
def log_message(msg_type, recipient, subject, message):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO logs (type, recipient, subject, message, sent_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (msg_type, recipient, subject, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# ========= ইমেইল পাঠানোর ফাংশন (একাধিককে পাঠাতে পারবে) =========
def send_email(sender, password, recipients, subject, content):
    recipients_list = [email.strip() for email in recipients.split(',')]
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients_list)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        # প্রতিটি রিসিপিয়েন্টের জন্য লগ
        for r in recipients_list:
            log_message('email', r, subject, content)
        return f"✅ Email sent to {len(recipients_list)} recipient(s)."
    except Exception as e:
        return f"❌ Email failed: {e}"

# ========= SMS পাঠানোর ফাংশন (একাধিককে পাঠাতে পারবে) =========
def send_sms(api_key, numbers, message):
    numbers_list = [num.strip() for num in numbers.split(',')]
    results = []
    for num in numbers_list:
        url = "https://bulksmsbd.net/api/smsapi"
        payload = {
            "api_key": api_key,
            "number": num,
            "message": message,
            "senderid": "8809612446XXX"
        }
        try:
            response = requests.post(url, data=payload)
            results.append(f"✅ SMS sent to {num}")
            log_message('sms', num, '', message)
        except Exception as e:
            results.append(f"❌ SMS failed for {num}: {e}")
    return "\n".join(results)

# ========= GUI ও ইন্টারঅ্যাকশন =========
def send_both():
    email_status = send_email(
        email_user.get(),
        email_pass.get(),
        email_to.get(),
        email_sub.get(),
        email_msg.get("1.0", tk.END).strip()
    )
    sms_status = send_sms(
        sms_api_key.get(),
        sms_number.get(),
        sms_msg.get("1.0", tk.END).strip()
    )
    status_label.config(text=f"{email_status}\n{sms_status}")

window = tk.Tk()
window.title("Message Hub")
window.geometry("450x700")

# Email ইনপুট ফিল্ডস
tk.Label(window, text="Your Email:").pack()
email_user = tk.Entry(window, width=50)
email_user.pack()

tk.Label(window, text="Password:").pack()
email_pass = tk.Entry(window, show="*", width=50)
email_pass.pack()

tk.Label(window, text="To (Emails):").pack()
email_to = tk.Entry(window, width=50)
email_to.pack()

tk.Label(window, text="Subject:").pack()
email_sub = tk.Entry(window, width=50)
email_sub.pack()

tk.Label(window, text="Email Message:").pack()
email_msg = tk.Text(window, height=7, width=50)
email_msg.pack()

# SMS ইনপুট ফিল্ডস
tk.Label(window, text="SMS API Key:").pack()
sms_api_key = tk.Entry(window, width=50)
sms_api_key.pack()

tk.Label(window, text="To (Phone Numbers):").pack()
sms_number = tk.Entry(window, width=50)
sms_number.pack()

tk.Label(window, text="SMS Message:").pack()
sms_msg = tk.Text(window, height=5, width=50)
sms_msg.pack()

# Send Button ও Status Label
tk.Button(window, text="Send Email & SMS", command=send_both).pack(pady=15)
status_label = tk.Label(window, text="", justify=tk.LEFT)
status_label.pack()

window.mainloop()