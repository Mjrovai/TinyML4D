#!/usr/bin/env python
# coding: utf-8

# 2- Query the Persistent RAG Database

import time
import warnings
import os
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain import hub

# Suppress LangSmith warnings
warnings.filterwarnings("ignore", 
                        message="API key must be provided when using hosted LangSmith API",
                        category=UserWarning)



# Define persistent directory for Chroma
PERSIST_DIRECTORY = "chroma_db"


# Initialize the LLM
local_llm = "llama3.2:3b"
llm = ChatOllama(model=local_llm, temperature=0)


def load_retriever():
    """Load the vector store from disk and create a retriever"""
    if not os.path.exists(PERSIST_DIRECTORY):
        raise FileNotFoundError(f"Database directory {PERSIST_DIRECTORY} not found. Please run create-database.py first.")
    
    print("Loading existing vector store...")
    
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(
        collection_name="rag-edgeai-eng-chroma",
        embedding_function=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(k=3)
    return retriever


def answer_question(question, retriever):
    """Generate an answer using the RAG system"""
    # Start timing
    start_time = time.time()
    
    # Retrieve relevant documents
    print(f"Question: {question}")
    print("Retrieving documents...")
    docs = retriever.invoke(question)
    docs_content = "\n\n".join(doc.page_content for doc in docs)
    print(f"Retrieved {len(docs)} document chunks")
    
    # Generate answer using RAG prompt
    print("Generating answer...")
    rag_prompt = hub.pull("rlm/rag-prompt")
    
    # Create the chain
    rag_chain = rag_prompt | llm | StrOutputParser()
    
    # Generate the answer
    answer = rag_chain.invoke({"context": docs_content, "question": question})
    
    # Calculate and print latency
    end_time = time.time()
    latency = end_time - start_time
    print(f"Response latency: {latency:.2f} seconds using model: {local_llm}")
    
    return answer


# Load the retriever once
retriever = load_retriever()


def interactive_mode():
    """Run an interactive query session"""
    try:
        # Load the retriever once
        retriever = load_retriever()
        
        print("==== RAG Query System ====")
        print("Type your questions and press Enter. Type 'quit' to exit.")
        
        while True:
            question = input("\nYour question: ")
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            print("\nGenerating answer...\n")
            answer = answer_question(question, retriever)
            
            print("\nANSWER:")
            print("="*50)
            print(answer)
            print("="*50)
    
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    interactive_mode()
