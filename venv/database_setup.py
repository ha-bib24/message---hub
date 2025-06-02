import sqlite3

def create_database():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        recipient TEXT NOT NULL,
        subject TEXT,
        message TEXT NOT NULL,
        sent_at TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    print("Database and table created successfully.")

if _name_ == "_main_":
    create_database()