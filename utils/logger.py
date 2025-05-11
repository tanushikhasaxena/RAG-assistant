import json
from datetime import datetime

def log_decision(query, tool, context_chunks=None):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "tool_used": tool,
        "context_snippets": [chunk.page_content[:100]+"..." for chunk in context_chunks] if context_chunks else []
    }
    with open("query_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
