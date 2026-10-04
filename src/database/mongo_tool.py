from pymongo import MongoClient
from langchain_core.tools import tool


client = MongoClient("mongodb://localhost:27017")

db = client["company_nosql"]
collection = db["employee_activity"]


@tool
def query_company_nosql(question: str) -> str:
    """
    Query MongoDB for employee project, skill, role, or city information.
    """

    question_lower = question.lower()

    # Search by employee name
    employees = ["rahul", "amit", "arjun"]

    for employee in employees:
        if employee in question_lower:
            document = collection.find_one(
                {"name": {"$regex": f"^{employee}$", "$options": "i"}},
                {"_id": 0}
            )

            if document:
                return str(document)

    # Search by city
    cities = ["bangalore", "mysore"]

    for city in cities:
        if city in question_lower:
            documents = list(
                collection.find(
                    {"city": {"$regex": f"^{city}$", "$options": "i"}},
                    {"_id": 0}
                )
            )

            if documents:
                return str(documents)

    return "No matching employee information found in MongoDB."