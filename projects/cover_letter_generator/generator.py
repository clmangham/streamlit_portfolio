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
    def __init__(self, resume_file, job_descrption_url, openai_api_key):
        self.resume_file = resume_file
        self.job_descrption_url = job_descrption_url
        self.openai_api_key = openai_api_key


    def cover_letter_generator(self):

        # Set up chat GPT model
        # _ = load_dotenv(find_dotenv())  # read local .env file with API Key
        llm_model = "gpt-3.5-turbo"  # Choose model

        llm = ChatOpenAI(temperature=0.5, model=llm_model, openai_api_key = self.openai_api_key)

        # Create prompt defining context
        prompt = ChatPromptTemplate.from_template(
            """Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}"""
        )

       # Create document chain with llm and contextual promp
        document_chain = create_stuff_documents_chain(llm, prompt)

        # -- RESUME (PDF) --
        # Generate temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(self.resume_file.getvalue())
            tmp_file_path = tmp_file.name

        # Load resume.pdf from temporary filepath
        loader = PDFPlumberLoader(
            tmp_file_path
        )
        pages = loader.load()

        # Split text and generate list of documents
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(pages)
        resume_list = [documents[0].page_content]

        # Set up keyword (BM25) retrieval for RESUME
        bm25_retriever = BM25Retriever.from_texts(
            resume_list, metadatas=[{"resume": 1}] * len(resume_list)
        )

        bm25_retriever.k = 2  # Return top k relevant results (for example 2 pages/chunks)

        # -- JOB DESCRIPTION (URL) --
        # Load job description from url
        loader = WebBaseLoader(self.job_descrption_url)
        data = loader.load()

        # I don't apply a text splitter here because of HTML. There is an html parser but it is limited by requiring website specific constraints
        job_description_list = [data[0].page_content]

        # Use FAISS (similarity search) and openAI embedding for semantic search of job description
        embedding = OpenAIEmbeddings(openai_api_key = self.openai_api_key)
        faiss_vectorstore = FAISS.from_texts(
            job_description_list,
            embedding,
            metadatas=[{"job_description": 2}] * len(job_description_list),
        )

        faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 2})

        # -- ENSEMBLE RETRIEVER --
        # initialize the ensemble retriever with equal weight for both retreivers
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
        )

        # Create retrieval chain wit ensemble retriever and document_chain defining context
        retrieval_chain_ensemble = create_retrieval_chain(ensemble_retriever, document_chain)

        # Prover prompt for cover letter prompt to retrieval chain
        prompt_input = "Write a cover letter for the provided resume and job description."


        # Invoke chain for response
        response = retrieval_chain_ensemble.invoke(
            {"input": prompt_input}
        )

        return response["answer"]