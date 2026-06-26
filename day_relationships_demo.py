import sqlite3
from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__, template_folder='day_relationships_templates')
app.secret_key = 'demo_secret_key'  # Needed for flashing messages

def get_db():
    """Database connection"""
    conn = sqlite3.connect('day_relationships.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

def init_db():
    conn = get_db()
    #Table 1 - subjects(the "lookup" sheet)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    #Table 2 - students(stores subject_id, NOT the subject name)
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS students (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     subject_id INTEGER,
                     FOREIGN KEY (subject_id) REFERENCES subjects(id)
                 )
    ''')
    # Foreign Key - This line tells the database :
    # 'subject_id here must match a real id in the subjects table'
    # Its a promise of data correctness. 
    
    conn.commit()
    conn.close()
    
@app.route("/")
def home():
    conn = get_db()
    
    # - Without JOIN - we only get subject_id, not the name
    students_raw = conn.execute('SELECT * FROM students').fetchall()
    # You can see the subject_id, but not the name of the subject
    # Not very useful for the user.
    
    # - With JOIN - we get the subject name too
    students_joined = conn.execute('''
        SELECT students.name AS student_name,
                subjects.name AS subject_name    
        FROM students
           JOIN subjects ON students.subject_id = subjects.id
    ''').fetchall()
    
    # JOIN - combine rows from two tables
    # ON students.subject_id = subjects.id - Matching rule
    # only combine rows where the subject_id in students matches the id in subjects
    
    conn.close()
    return render_template("home.html", students_raw=students_raw, students_joined=students_joined)

@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        name = request.form['name'].strip()
        conn = get_db()
        conn.execute('INSERT INTO subjects (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        flash(f"Subject '{name}' added successfully!")
        return redirect(url_for('home'))
    return render_template("add_subject.html")

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    conn= get_db()
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    # subjects list - needed to populate the dropdown in the form
    if request.method == "POST":
        name = request.form['name'].strip()
        subject_id = request.form['subject_id']
        conn.execute('INSERT INTO students (name, subject_id) VALUES (?, ?)', (name, subject_id))
        conn.commit()
        conn.close()
        flash(f"Student '{name}' added successfully!")
        return redirect(url_for('home'))
    return render_template("add_student.html", subjects=subjects)

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True, port=5004)
    