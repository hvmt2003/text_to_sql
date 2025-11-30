from langchain_community.utilities import SQLDatabase

uri = "mysql+pymysql://root:R%40njutr1p%40th1@localhost:3306/text_to_sql"

try:
    db = SQLDatabase.from_uri(uri)
    print("Connection successful!")
    print("Tables:", db.get_usable_table_names())
except Exception as e:
    print("Error:", e)
