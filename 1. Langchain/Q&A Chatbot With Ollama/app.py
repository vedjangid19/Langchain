import streamlit as st
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
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

def generate_response(question, llm, temperature, max_tokens):


    llm_model = Ollama(
        model=llm,
        # temperature=temperature,
        # max_tokens=max_tokens,
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


llm = st.sidebar.selectbox("Select An Open Source Model from Ollama", options=["llama3.1", "llama2", "gemma2:2b"])
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

st.write("Ask Any Question")
user_input = st.text_input("")

if user_input:
    answer = generate_response(
        llm=llm,
        temperature=temperature,
        max_tokens=max_tokens,
        question=user_input
    )
    st.write(answer)
else:
    st.write("Please provide the query.")