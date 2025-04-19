import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.vectorstores import FAISS

 

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm_model = ChatGroq(model="Llama3-8b-8192", groq_api_key=groq_api_key)

prompt = ChatPromptTemplate.from_template(
    """Answer the Question based on the provide context only. please provide the most accurate response based on the question
    <context>
    {context}
    </context>

    Question: {input}
    """
)

def create_vector_embeddings():
    if "vectors" not in st.session_state:
        st.session_state.Ollama_embeddings = OllamaEmbeddings()
        st.session_state.hf_embeddings = HuggingFaceEmbeddings(model_name="all-miniLM-L6-v2")
        st.session_state.Ollama_embeddings = OpenAIEmbeddings()

        st.session_state.loader = PyPDFDirectoryLoader("research_paper")
        st.session_state.docs = st.session_state.loader.load()

        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

        st.session_state.splitted_docs = st.session_state.text_splitter.split_documents(st.session_state.docs)

        st.session_state.vector_store = FAISS.from_documents(
            st.session_state.splitted_docs,
            st.session_state.Ollama_embeddings
        )

user_prompt = st.text_input("Enter your Query from The research Paper.")

if st.button("Document Embedding"):
    create_vector_embeddings()
    st.write("Vector Database is ready")


if user_prompt:

    documemt_chain = create_stuff_documents_chain(
        llm_model,
        prompt
        )
    
    retriver = st.session_state.vector_store.as_retriever()

    retriver_chain = create_retrieval_chain(
        retriver,
        documemt_chain
    )

    response = retriver_chain.invoke(
        {
            "input": user_prompt
        }
    )
    print(response)
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("---------------------------")

