import sqlite3
from flask import Flask, render_template, request, flash
app = Flask(__name__)
app.secret_key = "linkkiwi2026"  # Needed for flashing messages 

# 2 functions
def get_db():
   """Database connection""" 
   conn = sqlite3.connect('myproject.db')
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
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)