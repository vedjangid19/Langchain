import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
import uvicorn

load_dotenv()

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple api server using langchain runnale iterface."
)

groq_api_key = os.getenv('GROQ_API_KEY')

model = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

prompt = ChatPromptTemplate(
    [
        ("system", "Translate the following into {language}."),
        ("user", "{text}")
    ]
)

parser = StrOutputParser()

chain = prompt | model | parser

add_routes(
    app,
    chain,
    path="/chain"
)


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)

