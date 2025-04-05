from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

def load_pdf_and_create_vectorstore(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split()

    embeddings = OpenAIEmbeddings()
    qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        url="http://localhost:6333",  # Or your hosted Qdrant
        prefer_grpc=True,
        collection_name="pdf_docs"
    )
    return qdrant

def query_pdf(vectorstore, query):
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(query)
