from src.database.sql_tool import query_company_database


query = """
SELECT name, role
FROM employees
WHERE city = 'Bangalore'
"""

result = query_company_database.invoke(query)

print("\n========== SQL RESULT ==========\n")
print(result)