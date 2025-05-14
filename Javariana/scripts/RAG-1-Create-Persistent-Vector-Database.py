#!/usr/bin/env python
# coding: utf-8

# 1 - Create Persistent Vector Database for RAG
#  - Edge AI


import warnings
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Suppress LangSmith warnings
warnings.filterwarnings("ignore", 
                        message="API key must be provided when using hosted LangSmith API",
                        category=UserWarning)


# Vector Database

# Define persistent directory for Chroma
PERSIST_DIRECTORY = "chroma_db"


# PDF documents to include
pdf_paths = ["../datos/Alfaces-LSTM-GustavoCastro.pdf"]


# Define URLs for document sources
urls = [
    "https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/llm/llm.html",
    "https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/vlm/vlm.html"
]


def create_vectorstore():
    """Create the vector store with document data and persist it to disk"""
    print("Creating persistent vector store...")
    
    # Load documents from PDFs
    docs_list = []
    for path in pdf_paths:
        if os.path.exists(path):
            print(f"Loading PDF: {path}")
            loader = PyPDFLoader(path)
            docs_list.extend(loader.load())
        else:
            print(f"Warning: PDF file {path} not found")
    
    # Load documents from URLs
    print("Loading documents from URLs...")
    try:
        web_docs = []
        for url in urls:
            print(f"Loading URL: {url}")
            loader = WebBaseLoader(url)
            web_docs.extend(loader.load())
        docs_list.extend(web_docs)
    except Exception as e:
        print(f"Error loading URL documents: {e}")
    
    if not docs_list:
        print("Error: No documents were loaded. Check file paths and URLs.")
        return None
    
    print(f"Total documents loaded: {len(docs_list)}")
    
    # Split documents
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=300, chunk_overlap=30
    )
    doc_splits = text_splitter.split_documents(docs_list)
    print(f"Created {len(doc_splits)} document chunks")
    
    # Create embedding function
    print("Initializing embedding model...")
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    
    # Create and persist vectorstore to disk
    print("Creating vector database...")
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-edgeai-eng-chroma",
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    
    # Important: persist to disk
    vectorstore.persist()
    
    print(f"Vector store created and saved to {PERSIST_DIRECTORY}")
    print(f"Total document chunks indexed: {len(doc_splits)}")
    
    return vectorstore


# Check if database already exists
if os.path.exists(PERSIST_DIRECTORY):
    choice = input(f"Database already exists at {PERSIST_DIRECTORY}. Recreate? (y/n): ")
    if choice.lower() != 'y':
        print("Exiting without changes.")
        exit()
    
# Create the vector store
create_vectorstore()
print("Database creation complete!")


