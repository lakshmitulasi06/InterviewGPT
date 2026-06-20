import streamlit as st
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_vector_store(pdf_file):
    """
    Chunks the input question bank PDF and compiles it into an in-memory Chroma DB.
    """
    loader = PyPDFLoader(pdf_file)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    return vectordb

def generate_question(vectordb, profile_summary, context_history=""):
    """
    Uses vector matching to grab source questions and uses Llama-3 to write 
    a clean, relevant technical question or follow-up.
    """
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # Query vector store using candidate profile summary as keywords
    search_query = f"Interview questions about {str(profile_summary)}"
    docs = vectordb.similarity_search(search_query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    
    prompt = f"""
    You are an Elite Technical Interviewer conducting a mock interview for a 'GenAI and Prompt Engineering' internship.

    Reference Source Topics:
    {context}

    Candidate Profile:
    {str(profile_summary)}

    Interview Chat History So Far:
    {context_history}

    Your Task:
    Generate the next logical interview question. 
    - If there is no chat history, choose an introductory technical topic based on the reference source material that matches the candidate's skills.
    - If there is chat history, review the previous answer and ask a relevant technical follow-up question digging deeper into their knowledge.
    
    Return ONLY the question text. Do not add labels, headers, intro phrasing, or meta-commentary.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()