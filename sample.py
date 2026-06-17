# QUICK SQL Cheat Sheet -
# 
#   SELECT * FROM table_name;  -- Retrieve all records from a table
#   SELECT * FROM table_name ORDER BY column_name ASC;  -- Retrieve all records sorted by a column in ascending order
#   SELECT * FROM table_name WHERE marks >= 80;  -- Retrieve records where marks are greater than or equal to 80
#   SELECT * FROM table_name WHERE name LIKE 'A%';  -- Retrieve records where name starts with 'A'
#   SELECT COUNT(*) FROM table_name;  -- Count the number of records in a table
#   SELECT * FROM table_name LIMIT 5;  -- Retrieve only the first 5 records from a table

from flask import Flask


abort(400)  # Bad Request if something is wrong with the request
abort(401) # Unauthorized if user is not authenticated
abort(403) # Forbidden if user is authenticated but does not have permission
abort(404) # Not found - page or resource does not exist
abort(500) #Internal Server Error - something went wrong on the server side

EDIT - 2 routes - GET (fetch existing record) and POST (update record)



ADD -> INSERT --> DB -_> Flash --> redirect
VIEW -> SELECT --> CARDS  -> Stats
DETAILS -> SELECT WHERE ID --> DETAILS PAGE --> if not found -> 404
EDIT --> GET pre-fill --> POST UPDATE --> FLASH --> redirect
DELETE --> DELETE -->FLASH
404 --> ABORT(404) --> 404.html

Reply karo — A, B, C, ya D:
A — Flask + Templates + Bootstrap + Forms +
Database + CRUD sab working

GROUP A -
Challenge 1 - Search Feature , Add search bar on Navbar
Challenge 2 - Sort Feature - Name/ Marks/Attendance/Subject

    
B — Flask + DB working — CRUD mein kuch pending 
Step 1 - SELECT working - View students list



C — Flask + Templates working —
Database abhi nahi hua 


D — Flask bhi properly nahi chal raha


HTML -
div, h1, h2 , p, a , ul, li, table, tr,td, th, form, input, button, select

Search concepts -
User type: "Soham"

URL:localhost:5000/search?q=Soham

Flask receives : request.args.get('q') = "Soham"

SQL: SELECT * FROM students WHERE name LIKE '%Soham%'

Result: List of students whose names contain "Soham"

Filter concept -
Step 1 - Problem
200 students -  sirf computer science ke students ko dekhna hai

Step 2 - How it works?
User dropdown se "Computer Science" select karta hai
Form submit hota hai - GET method

URL - localhost:5000/students?subject=Computer+Science

Flask -
request.args.get('subject') = "Computer Science"

SQL query -
SELECT * FROM students WHERE subject = 'Computer Science'

Output - List of students enrolled in Computer Science subject


