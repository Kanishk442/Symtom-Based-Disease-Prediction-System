'''import mysql.connector
# Establish connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ktom2005",
    database="sample_db"
)
# Create cursor
cursor = connection.cursor()
# Execute query
cursor.execute("SELECT * FROM employees")
# Fetch and display results
results = cursor.fetchall()
for row in results:
    print(row)
# Close connection
cursor.close()
connection.close()'''

















import mysql.connector
# Establish connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="*****",  
    database="sample_db"  
)
# Create cursor
cursor = connection.cursor()
# Execute query
cursor.execute("SELECT * FROM employees")
# Fetch only one row
row = cursor.fetchone()
print("Single Employee Record (Using fetchone):")
print(row)
# Close connection
cursor.close()
connection.close()