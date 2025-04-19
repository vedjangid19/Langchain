import streamlit as st
import os
from dotenv import load_dotenv

from langchain.chains import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma, FAISS

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings


load_dotenv()

os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')
groq_api_key = os.getenv('GROQ_API_KEY')
embeddings = HuggingFaceEmbeddings(model_name="all-miniLM-L6-v2")
# embeddings = OpenAIEmbeddings()


st.title("Conversational Rag with PDF Upload and Chat History")
st.write("Upload PDF file and chat with their content")

api_key = st.text_input("Enter your Groq API Key", type="password")
session_id = st.text_input("Session ID", value="Default_Session")

if api_key:
    llm_model = ChatGroq(model="Llama3-8b-8192", groq_api_key=groq_api_key)

    if 'store' not in st.session_state:
        st.session_state.store = {}
    
    uploads_file = st.file_uploader("Choose A PDF File", type="pdf", accept_multiple_files=True)

    if uploads_file:
        documents = []

        for upload_file in uploads_file:
            temp_pdf = "temp.pdf"
            
            with open(temp_pdf, "wb") as file:
                file.write(upload_file.read())
                # file_name = upload_file.name


            loader = PyPDFLoader(temp_pdf)
            docs = loader.load()

            documents.extend(docs)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )


        splitted_docs = text_splitter.split_documents(documents)

        vectorstore_db = FAISS.from_documents(splitted_docs, embeddings)
        retriever = vectorstore_db.as_retriever()

        contextualize_que_system_prompt = (
            "given a chat history with latest user question which may refrence context in the chat history"
            "formulate a standalone question which can be understood without the chat history. do not answer the question"
            "just reformulate it if needed and otherwise return it as is"
        )
        contextualize_que_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_que_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("user", "{input}")
            ]
        )

        history_aware_retriever = create_history_aware_retriever(llm_model, retriever, contextualize_que_prompt)

        system_prompt = (
            "you are an assistance for question - answering task use"
            "the following pieces of retrieved context to answer the question. if you donot know the answer say that you"
            "don't know use three sentances maximum and keep the answer concise"
            "\n\n"
            "{context}"
        )

        que_ans_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("user", "{input}")
            ]
        )

        que_ans_chain = create_stuff_documents_chain(llm_model, que_ans_prompt)

        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            que_ans_chain
        )

        def get_session_history(session_id:str)->BaseChatMessageHistory:
            
            if session_id not in st.session_state.store:
                st.session_state.store[session_id] = ChatMessageHistory()

            return st.session_state.store[session_id]
        
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        user_input = st.text_input("your Question:")

        if user_input:
            print("question answer", user_input)
            session_history = get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {
                    "input": user_input
                },
                config={"configurable": {"session_id": session_id}}
            )
            print("response: ", response)
            st.write(st.session_state.store)
            st.write(response['answer'])
            st.write(session_history.messages)
else:
    st.warning("Please Enter The Groq API Key")
