import sqlite3
from datetime import datetime

def log_message(msg_type, recipient, subject, message):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    sent_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    c.execute('''
    INSERT INTO logs (type, recipient, subject, message, sent_at)
    VALUES (?, ?, ?, ?, ?)
    ''', (msg_type, recipient, subject, message, sent_at))

    conn.commit()
    conn.close()
    print(f"Logged {msg_type} to {recipient} at {sent_at}")