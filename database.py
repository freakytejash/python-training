import os
import sqlite3
from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = "linkkiwi2026"  # Needed for flashing messages 

#Absoulute path - Always with app.py folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'myproject.db')
# 2 functions
def get_db():
   """Database connection""" 
   conn = sqlite3.connect(DB_PATH)
   conn.row_factory = sqlite3.Row  # To access columns by name
   return conn

def init_db():
    
    
    
    
    """Create table"""""
    conn = get_db()
    # Create students table if it doesn't exist
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll INTEGER NOT NULL,
                    marks INTEGER NOT NULL,
                    subject TEXT NOT NULL,
                    attendance INTEGER DEFAULT 0
                 )
                    ''')
    
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS users (
                 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                 )
                    ''')    
    try:
       conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
    except Exception:
        # Column already exists
        pass
     
    conn.execute('''
                  CREATE TABLE IF NOT EXISTS subjects (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL UNIQUE
                     )
                     '''
                  )
    default_subjects = ['Java', 'C++', 'Python', 'Operating Systems', 'Data Structures', 'Database Management Systems', 'Computer Networks']

    for subject in default_subjects:
         try:
               conn.execute("INSERT INTO subjects (name) VALUES (?)", (subject,))
         except sqlite3.IntegrityError:
               # Subject already exists, ignore the error
               pass
                 
    conn.commit()
    conn.close()
    
init_db()  # Initialize the database
if __name__ == "__main__":
    app.run(debug=True)