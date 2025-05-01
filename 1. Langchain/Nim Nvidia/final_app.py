import streamlit as st
import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.output_parsers import StructuredOutputParser
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')

llm = ChatNVIDIA(
    model="meta/llama-3.3-70b-instruct",
)

def embedding_vectorstore():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = NVIDIAEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
        st.session_state.final_documnets = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documnets, st.session_state.embeddings)


st.title("NVIDIA NIM Demo")
prompt = PromptTemplate.from_template(
    """
    Answer the question based on provided context only. Please provide the most accurate response based on the question

    <context>
    {context}
    </context>
    Question: {input}

    """
)

user_query = st.text_input("Enter your question from documents.")

if st.button("document Embedding"):
    embedding_vectorstore()
    st.write("FAISS vector store DB is ready using Nvidia Embedding.")

if user_query:
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    retriever = st.session_state.vectors.as_retriever()

    retriever_chain = create_retrieval_chain(retriever=retriever, combine_docs_chain=document_chain)

    response = retriever_chain.invoke({"input": user_query})
    st.write(response['answer'])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")