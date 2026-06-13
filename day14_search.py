# day 14)search
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'Linkkiwi2026'

#Same 2 functions as before
def get_db():
    conn = sqlite3.connect('practise.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        marks INTEGER DEFAULT 0
        subject TEXT NOT NULL,
        attendance INTEGER DEFAULT 0
    )''')
    
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Tanuja', 85, 'Math', 90)")
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Pratiksha', 78, 'Science', 85)")
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Shlok', 92, 'English', 95)")
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Lucky', 65, 'History', 80)")
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Aarav', 88, 'Math', 92)")
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Ishita', 74, 'Science', 78)")
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Rohan', 95, 'English', 98)")
    conn.execute("INSERT OR IGNORE INTO students (name, marks, subject, attendance) VALUES ('Meera', 81, 'History', 85)")
    conn.commit()
    conn.close()