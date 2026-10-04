import sqlite3


DATABASE_PATH = "company.db"


# Connect to SQLite database
connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


# Create employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    role TEXT NOT NULL,
    experience INTEGER
)
""")


# Insert sample employees
employees = [
    (1, "Rahul", "Bangalore", "Python Developer", 3),
    (2, "Priya", "Mumbai", "Data Analyst", 2),
    (3, "Amit", "Bangalore", "AI Engineer", 4),
    (4, "Sneha", "Pune", "Tester", 3),
    (5, "Arjun", "Bangalore", "Python Developer", 5),
    (6, "Neha", "Delhi", "Data Scientist", 4),
]


cursor.executemany("""
INSERT OR REPLACE INTO employees
(id, name, city, role, experience)
VALUES (?, ?, ?, ?, ?)
""", employees)


# Save changes
connection.commit()


print("Database created successfully.")

# Show data
cursor.execute("SELECT * FROM employees")

rows = cursor.fetchall()

for row in rows:
    print(row)


connection.close()