import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentType
from pathlib import Path
import sqlite3
from sqlalchemy import create_engine


load_dotenv()

st.set_page_config(page_title="Langchain Chat with SQL Database.")
st.title("Langchain Chat with SQL Database.")

LOCAL_DB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = [
    "Connect Your MYSQL Database",
    "Use SQlite3 Database students.db"
]

selected_opt = st.sidebar.radio("Choose the Database which you want to chat", options=radio_opt)

if radio_opt.index(selected_opt) == 0:
    db_uri = MYSQL
    mysql_hostname = st.sidebar.text_input("Provide MYSQL Hostname")
    mysql_user = st.sidebar.text_input("MYSQL user")
    mysql_password = st.sidebar.text_input("MYSQL password", type="password", value="")
    mysql_database_name = st.sidebar.text_input("MYSQL DB Name")

else:
    db_uri = LOCAL_DB

api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if not db_uri:
    st.info("Please Enter The Database Info and URI")

if not api_key:
    st.info("Please Add your Groq API Key.")

llm = ChatGroq(
    model="Llama3-8b-8192",
    groq_api_key=api_key,
    streaming=True
)


# @st.cache_resource(ttl="2h")
def configure_database(db_uri, mysql_user=None, mysql_hostname=None, mysql_password=None, mysql_database_name=None):
    if db_uri == MYSQL:
        if not (mysql_hostname and mysql_database_name and mysql_user):
            st.error("Please provide all MySQL Details")
            st.stop()

        print("db_uri:",db_uri)
        try:
            engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_hostname}/{mysql_database_name}")
            db = SQLDatabase(engine)
            return db
        except Exception as e:
            print("error: ",e)
            st.error(f"Failed to connect to MySQL: {e}")
            st.stop()
        
    elif db_uri == LOCAL_DB:
        db_file_path = (Path(__file__).parent/"students.db").absolute()
        # print("db_file_path:",db_file_path)
        creator = lambda:sqlite3.connect(f"file:{db_file_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    
if db_uri == MYSQL:
    db = configure_database(
        db_uri=db_uri,
        mysql_user=mysql_user,
        mysql_hostname=mysql_hostname,
        mysql_password=mysql_password,
        mysql_database_name=mysql_database_name
        )
else:
    db = configure_database(db_uri=db_uri)


toolkit = SQLDatabaseToolkit(
    llm=llm,
    db=db,
)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "How can I help you?"
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

user_query = st.chat_input(placeholder="Ask Any Query From Database.")

if user_query:
    st.session_state.messages.append(
        {"role": "user", "content":user_query}
    )

    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cbh = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[st_cbh])

        st.session_state.messages.append({"role": "assistance", "content": response})
        st.write(response)

