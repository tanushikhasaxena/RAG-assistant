import streamlit as st
from rag_agent import initialize_rag
from tools import calculator_tool, hybrid_retriever
from utils.logger import log_decision
import re
import sys
from huggingface_hub import hf_hub_download
from urllib.parse import urlparse
from rag_agent import initialize_rag
from langchain_community.llms import Ollama

def _cached_download_wrapper(url: str, **kwargs):
    """Convert legacy 'url' parameter to modern 'repo_id'/'filename' format"""
    parsed = urlparse(url)
    repo_id = f"{parsed.netloc}/{parsed.path.split('/')[1]}/{parsed.path.split('/')[2]}"
    filename = parsed.path.split('/')[-1]
    return hf_hub_download(repo_id=repo_id, filename=filename, **kwargs)

sys.modules['huggingface_hub'].cached_download = _cached_download_wrapper

llm = Ollama(
    model="tinyllama",
    base_url="http://localhost:11435",  
    temperature=0.7
)
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = initialize_rag()

st.title("Open-Source RAG Assistant")
query = st.text_input("Ask anything:")

if query:
    if re.search(r'\b(calculate|math)\b', query, re.I):
        tool = "Calculator"
        answer = calculator_tool(query)
        context_chunks = None
    else:
        tool = "RAG"
        context_chunks = hybrid_retriever(query, st.session_state.vector_store)
        context_text = "\n".join([chunk.page_content for chunk in context_chunks])
        answer = llm(f"Context: {context_text}\nQuestion: {query}")
    log_decision(query, tool, context_chunks)
    st.subheader(f"Tool Used: {tool}")
    st.write("**Answer:**", answer)
    if context_chunks:
        st.divider()
        st.subheader("Retrieved Context")
        for i, chunk in enumerate(context_chunks, 1):
            st.write(f"Chunk {i}: {chunk.page_content[:200]}...")
