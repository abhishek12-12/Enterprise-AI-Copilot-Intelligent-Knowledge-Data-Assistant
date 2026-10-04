import sqlite3

from langchain_core.tools import tool


DATABASE_PATH = "company.db"


@tool
def query_company_database(question: str) -> str:
    """
    Answer questions about the employee database.

    The tool supports questions about employee count,
    employee location, employee roles, and experience.
    """

    question_lower = question.lower()

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:

        # -----------------------------------------
        # Employee count by city
        # -----------------------------------------

        if "how many employees" in question_lower:

            cities = [
                "bangalore",
                "mumbai",
                "pune",
                "delhi"
            ]

            for city in cities:

                if city in question_lower:

                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM employees
                        WHERE city = ?
                        """,
                        (city.title(),)
                    )

                    count = cursor.fetchone()[0]

                    return (
                        f"There are {count} employees "
                        f"in {city.title()}."
                    )


        # -----------------------------------------
        # List employees by city
        # -----------------------------------------

        if (
            "employees in" in question_lower
            or "employees are in" in question_lower
            or "which employees" in question_lower):
    
            cities = [
                "bangalore",
                "mumbai",
                "pune",
                "delhi"
            ]

            for city in cities:

                if city in question_lower:

                    cursor.execute(
                        """
                        SELECT name, role
                        FROM employees
                        WHERE city = ?
                        """,
                        (city.title(),)
                    )

                    rows = cursor.fetchall()

                    if not rows:
                        return f"No employees found in {city.title()}."

                    result = [
                        f"{name} - {role}"
                        for name, role in rows
                    ]

                    return (
                        f"Employees in {city.title()}:\n"
                        + "\n".join(result)
                    )


        # -----------------------------------------
        # Show all employees
        # -----------------------------------------

        if "all employees" in question_lower:

            cursor.execute(
                """
                SELECT name, city, role, experience
                FROM employees
                """
            )

            rows = cursor.fetchall()

            result = []

            for name, city, role, experience in rows:

                result.append(
                    f"{name} | {city} | {role} | "
                    f"{experience} years"
                )

            return "\n".join(result)


        return (
            "I can currently answer questions about "
            "employee counts, locations, roles, and experience."
        )

    except Exception as e:

        return f"Database error: {str(e)}"

    finally:

        connection.close()