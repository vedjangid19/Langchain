import os
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain.prompts import PromptTemplate
import streamlit as st
import validators
import pydantic
from urllib.parse import urlparse, parse_qs

def get_youtube_video_id(url):
    parsed_url = urlparse(url)

    # For standard YouTube URLs
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]

    # For shortened youtu.be URLs
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path.lstrip('/')

    return None

# Patch model rebuilding for Groq (avoids BaseCache issues)
try:
    ChatGroq.model_rebuild(force=True)
except pydantic.errors.PydanticUndefinedAnnotation:
    pass


st.set_page_config(page_title="Langchain Summarize text from youtube video and website")
st.title("Langchain Summarize text from youtube video and website")
st.subheader("Summarize URL")

prompt_template = "provide a summary of the following content in import bullet points which are in words: {text}"

prompt = PromptTemplate(
    input_variables=['text'],
    template=prompt_template
)

with st.sidebar:
    groq_api_key = st.text_input("Enter Your Groq API Key", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")

# Rebuild the model to resolve incomplete definitions
# ChatGroq.model_rebuild()

if not groq_api_key:
    st.error("Please Add your Groq API key.")
else:
    llm = ChatGroq(
        model="Gemma2-9b-It",
        groq_api_key=groq_api_key
    )


if st.button("Summarize the content from youtube video or website"):
    if not groq_api_key or not generic_url.strip():
        st.error("Please Add Groq API key or URL")
    elif not validators.url(generic_url):
        st.error("Provide valid URL. It can be youtube video url or website url.")
    else:
        try:
            with st.spinner("Waiting..."):
                if "youtube.com" in generic_url.lower():
                    video_id = get_youtube_video_id(generic_url)
                    if video_id:
                        loader = YoutubeLoader(video_id=video_id)
                    else:
                        st.error("Please add avlid youtube URL. In this url video id is wrong")
                else:
                    loader = UnstructuredURLLoader(
                        # ssl_verify=False,
                        urls=[generic_url],
                        # headers={}#{"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                        )
                
                docs = loader.load()

                chain = load_summarize_chain(
                    chain_type="stuff",
                    llm=llm,
                    prompt=prompt
                )

                output_summary = chain.run(docs)
                print("output summary:", output_summary)
                st.success(output_summary)
        except Exception as e:
            print(f"Exception occured: {e}")
            st.error(f"Exception occured: {e}")
