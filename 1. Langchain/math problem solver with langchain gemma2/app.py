import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain, LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.callbacks import StreamlitCallbackHandler
from langchain.utilities import WikipediaAPIWrapper


load_dotenv()

st.set_page_config(page_title="Text to math solver and data search assisatnant.")
st.title("Text to math problem solver using Gemma2")

groq_api_key = st.sidebar.text_input("Please add your groq api key", type="password")

if not groq_api_key:
    st.error("Please add your groq api key")
    st.stop()

llm = ChatGroq(
    model="Gemma2-9b-It",
    groq_api_key=groq_api_key
)

# initialize the tools

wikipedia_wrapper = WikipediaAPIWrapper()

wiki_tool = Tool(
    name="wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the internet to find the vatious information on the topics mentioned."
)

# initialize math tool
math_chain = LLMMathChain.from_llm(llm=llm)

calculator = Tool(
    func=math_chain.run,
    name="calculator",
    description="A tool for answering math related question. only mathematical expression need to be provided"
)

prompt = """you are agent tasked for solving user mathemtical question.logically arrive at the solution and provide a detailed explaination and display it point wise for the question below:\n Question:{question}
"""

prompt_template = PromptTemplate(input_variables=['question'], template=prompt)

# combine all the tools into chain

chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="reasoning",
    func=chain.run,
    description="a tool for answering logic based and reasoning questions"
)


# initialize the agent

agent = initialize_agent(
    tools=[wiki_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state['messages'] = [{"role":"assistant", "content": "Hi, I'm a math chatbot who can answer all your math questions."}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])



# ########## Normal without showing Thinking of Agent ###############
# user_query = st.text_area("Enter your question", "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

# if st.button("find my answer"):
#     if user_query:
#         with st.spinner("generate response..."):
#             st.session_state.messages.append(
#                 {
#                     "role": "user",
#                     "content": user_query
#                 }
#             )

#             st.chat_message("user").write(user_query)

#             streamlit_callback_handler = StreamlitCallbackHandler(
#                 st.container(),
#                 expand_new_thoughts=False
#             )

#             response = agent.run(st.session_state.messages, callbacks=[streamlit_callback_handler])

#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": response
#             })

#             st.write(response)
#     else:
#         st.warning("please enter the question")



# ################### showing Thinking of Agent ####################
user_query = st.chat_input("Enter Your Math Question: ")

# if st.button("find my answer"):
if user_query:
    with st.spinner("generate response..."):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_query
            }
        )

        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            streamlit_callback_handler = StreamlitCallbackHandler(
                st.container(),
                expand_new_thoughts=False
            )

            response = agent.run(user_query, callbacks=[streamlit_callback_handler])

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.write(response)
else:
    st.warning("please enter the question")
