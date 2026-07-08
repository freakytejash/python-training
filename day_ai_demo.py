from groq import Groq

client = Groq(api_key="YOUR_API_KEY")

student_name = "Sakshi"
student_marks = 40
student_subject = "DBMS"

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

print(tip)
