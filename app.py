from flask import Flask, render_template, request, flash

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
    return render_template("home.html", students=students)  # ← fixed


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/students")
def students_page():

    return render_template("students.html", students=students)


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
        # #new student dictionary
        new_student = {"name": name, "marks": int(marks)}
        students.append(new_student)
        # Flash message to user
        flash(f"Student {name} added successfully!", "success")
        print(f"Updated students list: {students}")
    return render_template("add_students.html")


if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)
