
from rank_bm25 import BM25Okapi 
import re
import numexpr

def hybrid_retriever(query, vector_store, k=3):

    corpus = list(vector_store.docstore._dict.values())
    tokenized_corpus = [doc.page_content.split() for doc in corpus]
    
    bm25 = BM25Okapi(tokenized_corpus)
    keyword_results = bm25.get_top_n(query.split(), corpus, n=k//2)
    vector_results = vector_store.similarity_search(query, k=k//2)
    
    seen = set()
    deduped_chunks = []
    for chunk in keyword_results + vector_results:
        content_hash = hash(chunk.page_content)
        if content_hash not in seen:
            seen.add(content_hash)
            deduped_chunks.append(chunk)
    return deduped_chunks

import re
import numexpr

def calculator_tool(query: str) -> str:
    """Handles math calculations from natural language queries"""
    try:
        # Extract math expression using regex
        match = re.search(r'(\d+[\+\-\*\/]\d+)', query)
        if not match:
            return "Could not find a valid math expression"
            
        expression = match.group(1)
        result = numexpr.evaluate(expression).item()
        return f"{expression} = {result}"
        
    except Exception as e:
        return f"Calculation error: {str(e)}"
