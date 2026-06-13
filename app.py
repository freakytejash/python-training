from flask import Flask, abort, redirect, render_template, request, flash, url_for

from database import get_db, init_db

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

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)
    