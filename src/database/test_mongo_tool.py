from mongo_tool import query_company_nosql


result = query_company_nosql.invoke(
    {"question": "Tell me about Rahul"}
)

print("\nMONGODB TOOL RESULT")
print(result)