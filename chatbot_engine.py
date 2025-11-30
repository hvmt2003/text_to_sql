import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase

load_dotenv()

# 1) Database connection (PyMySQL)
DB_URI = "mysql+pymysql://root:R%40njutr1p%40th1@localhost:3306/text_to_sql"
db = SQLDatabase.from_uri(DB_URI)

# 2) Gemini LLM - use a model your API key supports
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Prompt template
SQL_PROMPT = """
You are an expert MySQL assistant.
Given a natural language question and the given schema,
generate a correct, executable SQL query.

RULES:
- Only output SQL. No explanation.
- No backticks.
- Table names and column names must match exactly.
"""

def generate_sql(question: str):
    prompt = f"{SQL_PROMPT}\n\nDatabase Schema:\n{db.get_table_info()}\n\nUser question: {question}\n\nSQL Query:"
    sql = llm.invoke(prompt).content
    return sql.strip()

print("\n🔥 Text-to-SQL Chatbot READY — Ask your question:\n")

while True:
    q = input("You: ").strip()

    if q.lower() in ("exit", "quit"):
        break

    try:
        sql_query = generate_sql(q)
        print("\nGenerated SQL:\n", sql_query)
        
        result = db.run(sql_query)
        print("\nResult:\n", result, "\n")

    except Exception as e:
        print("\n❌ Error:", e, "\n")
