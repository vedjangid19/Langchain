import os
from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT')
os.environ['LANGCHAIN_OLLAMA_PROJECT'] = os.getenv('LANGCHAIN_OLLAMA_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['USER_AGENT'] = 'myagent'

prompt = ChatPromptTemplate(
    [
        ("system", "You are a helpfull assistant. Please respond to the question asked."),
        ("user", "Question:{question}")
    ]
)

llm = Ollama(model="llama3.1")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

st.title("Simple Chat bot Using Ollama (llama 3)")
input_text = st.text_input("Ask Any Question Which you have in mind?")

if input_text:
    response = chain.invoke({"question": input_text})
    st.write(response)


