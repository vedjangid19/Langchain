import os
from pinecone import ServerlessSpec, Pinecone
from dotenv import load_dotenv

load_dotenv()


index_name = "hybrid-search-langchain-pinecone2"
api_key = os.getenv('PINECONE_API_KEY')
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')


pinecone_obj = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

if index_name not in pinecone_obj.list_indexes().names():
    pinecone_obj.create_index(
        name=index_name,
        dimension=384,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pinecone_obj.Index(index_name)



from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder
from langchain_community.retrievers import PineconeHybridSearchRetriever


embeddings = HuggingFaceEmbeddings(model_name="all-miniLM-L6-v2")
bm25_encoder = BM25Encoder().default()

sentences=[
    "In 2023, I visited Paris",
    "In 2022, I visited New York",
    "In 2021, I visited New Orleans",
]

bm25_encoder.fit(sentences)

# store value in json file
bm25_encoder.dump("bm25_values.json")

retriever = PineconeHybridSearchRetriever(
    embeddings=embeddings,
    sparse_encoder=bm25_encoder,
    index=index
)

retriever.add_texts(sentences)

result = retriever.invoke("what city did i visit last")
