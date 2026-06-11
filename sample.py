# QUICK SQL Cheat Sheet -
# 
#   SELECT * FROM table_name;  -- Retrieve all records from a table
#   SELECT * FROM table_name ORDER BY column_name ASC;  -- Retrieve all records sorted by a column in ascending order
#   SELECT * FROM table_name WHERE marks >= 80;  -- Retrieve records where marks are greater than or equal to 80
#   SELECT * FROM table_name WHERE name LIKE 'A%';  -- Retrieve records where name starts with 'A'
#   SELECT COUNT(*) FROM table_name;  -- Count the number of records in a table
#   SELECT * FROM table_name LIMIT 5;  -- Retrieve only the first 5 records from a table

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

