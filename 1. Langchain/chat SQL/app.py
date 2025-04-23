import streamlit as st
import os
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from dotenv import load_dotenv


st.set_page_config(page_title="Langchain chat with SQL Database")
st.title("Langchain chat with SQL Database")

LOCAL_DB = "USE_LOCAL_DB"
MYSQL = "USE_MYSQL_DB"


