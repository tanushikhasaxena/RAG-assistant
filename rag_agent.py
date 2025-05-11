import sys
import os
from huggingface_hub import hf_hub_download
from urllib.parse import urlparse
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader

def _cached_download_wrapper(url: str, **kwargs):
    """Convert legacy 'url' parameter to modern 'repo_id'/'filename' format"""
    parsed = urlparse(url)
    repo_id = f"{parsed.netloc}/{parsed.path.split('/')[1]}/{parsed.path.split('/')[2]}"
    filename = parsed.path.split('/')[-1]
    return hf_hub_download(repo_id=repo_id, filename=filename, **kwargs)

sys.modules['huggingface_hub'].cached_download = _cached_download_wrapper



def initialize_rag():
    
    if not os.path.exists('./docs') or not os.listdir('./docs'):
        raise ValueError("The './docs' folder is empty! Please add at least one .txt file.")
   
    loader = DirectoryLoader('./docs', glob="**/*.txt")
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, 
        chunk_overlap=20
    )
    chunks = text_splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},  
    encode_kwargs={'normalize_embeddings': False}
)

    
    return FAISS.from_documents(chunks, embeddings)
