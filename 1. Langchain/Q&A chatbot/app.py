import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import openai
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHIN_TRACING_V2'] = "true"
os.environ['PROJECT_NAME'] = "Q&A-CHATBOT"

prompt = ChatPromptTemplate(
    [
        ("system", "you are a helpful chat assistance please provide answer based on user query."),
        ("user", "Question: {question}")
    ]
)

def generate_response(question, api_key, llm, temperature, max_tokens):

    openai.api_key = api_key
    llm_model = ChatOpenAI(
        model=llm,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    parser = StrOutputParser()
    chain = prompt | llm_model | parser
    response = chain.invoke(
        {
            "question": question
        }
    )

    return response

 
# Streamlit App
st.title("Enhanced Q&A ChatBot With OpenAI")
st.sidebar.title("Setting")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
llm = st.sidebar.selectbox("Select An OpenAI Model", options=["gpt-4", "gpt-4o", "gpt3.5-turbo"])
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

st.write("Ask Any Question")
user_input = st.text_input("")

if user_input:
    answer = generate_response(
        api_key=api_key,
        llm=llm,
        temperature=temperature,
        max_tokens=max_tokens,
        question=user_input
    )
    st.write(answer)
else:
    st.write("Please provide the query.")