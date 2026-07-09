from flask import Flask, render_template, request
import os
from groq import Groq

app = Flask(__name__, template_folder='day_ai_templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_tip', methods=['POST'])
def get_tip():
    student_name = request.form['name']
    student_marks = request.form['marks']
    student_subject = request.form['subject']

    client = Groq(api_key=os.environ.get("GROQ_API_KEY", "")) 

# Step 1 - Create a prompt.
    prompt = f"""
Student name: {student_name}
Subject: {student_subject}
Marks: {student_marks}/100
Please provide practical study tips, it should not be more than 2 lines.
"""

# Step 2 - API call to Groq API to get the response.
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role":"user",
         "content": prompt}
    ]
)

# Step 3 - Print the response.
    tip = response.choices[0].message.content

    return render_template('result.html', name=student_name, marks=student_marks, subject=student_subject, tip=tip)

if __name__ == '__main__':
    app.run(debug=True, port=5005)
    