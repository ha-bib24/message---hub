import sqlite3

def add_user(name, email):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
    except sqlite3.IntegrityError:
        print("User already exists.")
    conn.close()

def log_message(email, message):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
        cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, message))
        conn.commit()
    else:
        print("User not found.")
    conn.close()