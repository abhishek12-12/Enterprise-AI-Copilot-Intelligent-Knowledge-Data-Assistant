from src.llm.provider import get_llm
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    SystemMessage,
)

from src.rag.rag_tool import search_company_documents
from src.database.sql_tool import query_company_database
from src.database.mongo_tool import query_company_nosql


# ============================================================
# 1. Load Ollama model
# ============================================================

llm = get_llm()


# ============================================================
# 2. Register tools
# ============================================================

tools = [
    search_company_documents,
    query_company_database,
    query_company_nosql,
]

tools_by_name = {
    tool.name: tool
    for tool in tools
}


# ============================================================
# 3. Give tools to LLM
# ============================================================

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# 4. Main Agent Function
# ============================================================

def ask_agent(question: str) -> str:
    """
    Run the Enterprise AI Copilot agent
    and return the final answer.
    """

    messages = [
        SystemMessage(
    content="""
You are an Enterprise AI Copilot.

You have three tools:

1. search_company_documents

Use this for information contained in company documents,
resumes, PDFs, and other unstructured documents.

Examples:
- What skills are mentioned in my resume?
- Tell me about my project.
- What projects are mentioned in my resume?
- What technologies are mentioned in my resume?
- Tell me about my experience.
- What certifications are mentioned in my resume?

2. query_company_database

Use this ONLY for structured employee database questions
stored in SQLite.

Examples:
- How many employees are in Bangalore?
- Which employees are in Bangalore?
- Which employees work in Bangalore?
- What roles do employees have?
- How much experience does an employee have?

3. query_company_nosql

Use this ONLY for employee-specific information stored
in MongoDB.

Examples:
- Tell me about Rahul's skills.
- What projects has Rahul worked on?
- What are Rahul's certifications?
- Tell me Rahul's MongoDB information.

IMPORTANT ROUTING RULES:

- Questions about MY resume, MY projects, MY skills,
  MY experience, or information from the PDF MUST use
  search_company_documents.

- Questions asking about an employee's skills, projects,
  or certifications MUST use query_company_nosql.

- Employee count, city, role, and experience questions
  MUST use query_company_database.

- Do NOT use MongoDB just because the word "project"
  appears in the question.

- "Tell me about my project" means the user's resume/project
  information, so use search_company_documents.

- Always use the appropriate tool.
- Never invent information.
- Treat tool results as the source of truth.
"""
),
        HumanMessage(content=question)
    ]

    # ========================================================
    # 5. Ask LLM which tool to use
    # ========================================================

    response = llm_with_tools.invoke(messages)

    # ========================================================
    # 6. Check whether LLM requested a tool
    # ========================================================

    if response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_name = tool_call["name"]

        # ----------------------------------------------------
        # IMPORTANT:
        # Always use the actual user question for database
        # tools instead of trusting Llama to rewrite it.
        # ----------------------------------------------------

        if tool_name == "query_company_database":

            tool_args = {
                "question": question
            }

        elif tool_name == "query_company_nosql":

            tool_args = {
                "question": question
            }

        else:

            tool_args = tool_call["args"]

        # ----------------------------------------------------
        # Find selected tool
        # ----------------------------------------------------

        selected_tool = tools_by_name[tool_name]

        # ----------------------------------------------------
        # Execute tool
        # ----------------------------------------------------

        tool_result = selected_tool.invoke(tool_args)

        # ----------------------------------------------------
        # Structured database results are already final.
        # Do not send them back to Llama and risk hallucination.
        # ----------------------------------------------------

        if tool_name in [
            "query_company_database",
            "query_company_nosql"
        ]:

            return str(tool_result)

        # ----------------------------------------------------
        # RAG result goes back to Llama for final answer
        # ----------------------------------------------------

        messages.append(response)

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

        final_response = llm_with_tools.invoke(messages)

        return final_response.content

    # ========================================================
    # 7. No tool requested
    # ========================================================

    return response.content