from flask import Flask, render_template

app = Flask(__name__)

stud = [
    {"name": "Tanuja", "roll": 1, "marks": 85},
    {"name": "Pratiksha", "roll": 2, "marks": 78},
    {"name": "Shlok", "roll": 3, "marks": 92},
    {"name": "Lucky", "roll": 4, "marks": 65},
]

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Report page
@app.route('/students')
def students():
    return render_template('students.html', students=stud)


if __name__ == '__main__':
    print("INSIDE MAIN")
    app.run(debug=True)