from flask import Flask, abort, redirect, render_template, request, flash, session, url_for
from database import get_db, init_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "linkkiwi2026"  # Needed for flashing messages

students = [
    {"name": "Tanuja", "roll": 1, "marks": 85},
    {"name": "Pratiksha", "roll": 2, "marks": 78},
    {"name": "Shlok", "roll": 3, "marks": 92},
    {"name": "Lucky", "roll": 4, "marks": 65},
]

@app.route("/")
def home():
    conn = get_db()
    
    #All students from database
    students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    
    #Stats using count
    total = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    
    passed = conn.execute('SELECT COUNT(*) FROM students WHERE marks >= 45').fetchone()[0]
    
    excellent = conn.execute('SELECT COUNT(*) FROM students WHERE marks >= 90').fetchone()[0]
    
    conn.close()
    
    return render_template("home.html", students=students, 
                           total=total, passed=passed, excellent=excellent)



@app.route("/students")
def students_page():
    conn = get_db()
    students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    conn.close()
    return render_template("students.html", students=students)

# DELETE - remove by ID
@app.route('/delete/<int:id>')
def delete_student(id):
    if session.get('role') != 'admin':
        flash("Admins only!  You do not have permission", "danger")
        return redirect(url_for('home'))
    
    conn = get_db()
    
    # First check if it exists
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    if student is None:
        flash("Student not found", "danger")
        conn.close()
        return redirect(url_for('students_page'))
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully", "success")
    return redirect(url_for('students_page'))

@app.route("/students/<int:id>")
def student_detail(id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        flash("Student not found", "danger")
        return redirect(url_for("students_page"))
    
    return render_template("detail.html", student=student)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if session.get('role') != 'admin':
        flash("Admins only!  You do not have permission", "danger")
        return redirect(url_for('home'))
    
    if request.method == "POST":
        name = request.form["student_name"]
        marks = request.form["marks"]
        roll = request.form["roll"]
        subject = request.form["subject"]
        attendance = request.form["attendance"]
        if not name or not marks:
            flash('Please provide both name and marks', 'danger')
            return render_template("add_students.html")
        
        conn = get_db()
        conn.execute('''INSERT INTO students
                     (name,roll,marks,subject,attendance) VALUES(?,?,?,?,?)''',
                     (name, roll, int(marks), subject, int(attendance))
                     )
        conn.commit()
        conn.close()

        # Print to terminal
        print(f"Received new student: {name} with marks: {marks}")
        
        # Flash message to user
        flash(f"Student {name} added successfully!", "success")
        print(f"Updated students list: {students}")
    return render_template("add_students.html")

# EDIT - update by ID
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if session.get('role') != 'admin':
        flash("Admins only!  You do not have permission", "danger")
        return redirect(url_for('home'))
    
    conn = get_db()
    
    if request.method == 'POST':
        name = request.form['student_name']
        marks = request.form['marks']
        subject = request.form.get('subject', '')
        attendance = request.form.get('attendance', 0)
        
        if not name:
            flash('Name cannot be empty', 'danger')
            return redirect(url_for('edit_student', id=id))
        
        conn.execute('''UPDATE students SET name=?, marks=?, subject=?, attendance=? 
                     WHERE id=?''', (name, int(marks), subject, int(attendance), id))
        conn.commit()
        conn.close()
        flash(f'{name} updated successfully!', 'success')
        return redirect(url_for('students_page'))
    
# GET - fetch exisiting record
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if student is None:
        abort(404) # trigger 404.html
        
    return render_template('edit_student.html', student=student)

@app.route("/search")
def search():
    #step 1 - get query from URL
    
    q = request.args.get('q','')
    # request.args - GET parameters
    # 'q' - Form  - name = 'q'
    conn = get_db()
    
    if q:
        students = conn.execute('''SELECT * FROM students 
                                WHERE name LIKE ? 
                                OR SUBJECT LIKE ?
                                OR roll LIKE ?''',
                                (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
        
    else:
        students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    conn.close()
    return render_template("search.html", students=students, query=q)


@app.route('/filter')
def filter_students():
    #Values from URL
    subject = request.args.get('subject', '')
    grade = request.args.get('grade', '')

    conn = get_db()
    # Unique subjects for dropdown
    subjects = conn.execute('''SELECT DISTINCT subject FROM students
                            WHERE subject IS NOT NULL
                            AND subject != ""
                            ORDER BY subject ASC''').fetchall()    
    
    # Dynamically build query based on filters
        
    query = 'SELECT * FROM students WHERE 1=1'
    params = []
    if subject:
        query += ' AND subject = ?'
        params.append(subject)
    if grade =='excellent':
        query += ' AND marks >= 90'
    elif grade == 'good':
        query += ' AND marks >= 75 AND marks < 90'
    elif grade == 'average':
        query += ' AND marks >= 60 AND marks < 75'
    elif grade == 'poor':
        query += ' AND marks < 45'
        
    query += ' ORDER BY id DESC'
    students = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('filter.html', students=students, subjects=subjects, selected_subject=subject, selected_grade=grade)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db()
        # Check if username already exists
        existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Username already exists!', 'danger')
            conn.close()
            return render_template('register.html')
        
        hashed = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed, 'student'))
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user['role']
            flash(f'Welcome {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/subjects')
def subjects():
    conn= get_db()
    rows = conn.execute('''
            SELECT subjects.name AS subject_name, COUNT(students.id) AS student_count
            FROM subjects
            LEFT JOIN students ON students.subject = subjects.name
            GROUP BY subjects.name
            ORDER BY subjects.name
    ''').fetchall()
    conn.close()
    return render_template('subjects.html', rows=rows)
       
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)
    