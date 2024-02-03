import requests
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import WebBaseLoader
import streamlit as st
import tempfile

class CoverLetterGenerator:
    def __init__(self, resume_file, job_descrption_url):
        self.resume_file = resume_file
        self.job_descrption_url = job_descrption_url

    def cover_letter_generator(self):

        prompt_input = "Write a cover letter for the provided resume and job description."


        # Set up chat GPT model
        _ = load_dotenv(find_dotenv())  # read local .env file with API Key
        llm_model = "gpt-3.5-turbo"  # Choose model

        llm = ChatOpenAI(temperature=0.5, model=llm_model)
        # embeddings = OpenAIEmbeddings()

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(self.resume_file.getvalue())
            tmp_file_path = tmp_file.name


        # Load pdf
        loader = PDFPlumberLoader(
            tmp_file_path
        )
        pages = loader.load()

        # Create vector store
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(pages)
        resume_list = [documents[0].page_content]


        # vector = FAISS.from_documents(documents, embeddings)

        # Create document chain
        prompt = ChatPromptTemplate.from_template(
            """Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}"""
        )

        document_chain = create_stuff_documents_chain(llm, prompt)


    ### Create Download_description if == True 

        loader = WebBaseLoader(self.job_descrption_url)
        data = loader.load()

        job_description_list = [data[0].page_content]

        # Set up ensemble retrieval
        bm25_retriever = BM25Retriever.from_texts(
            resume_list, metadatas=[{"resume": 1}] * len(resume_list)
        )

        bm25_retriever.k = 2  # not sure what this does, num args? len list?

        embedding = OpenAIEmbeddings()
        faiss_vectorstore = FAISS.from_texts(
            job_description_list,
            embedding,
            metadatas=[{"job_description": 2}] * len(job_description_list),
        )
        faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 2})

        # initialize the ensemble retriever with equal weight
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
        )

        retrieval_chain_ensemble = create_retrieval_chain(ensemble_retriever, document_chain)

        response = retrieval_chain_ensemble.invoke(
            {"input": prompt_input}
        )

        return response["answer"]