# Open-Source RAG Assistant

## Steps to run

1. Install Python 3.8+ and [Ollama](https://ollama.com/download).
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ollama pull llama3:8b-instruct-q4_0
    ```
3. Put your text files in the `docs/` folder.
4. Start Ollama:
    ```
    ollama serve
    ```
5. Run the Streamlit app:
    ```
    streamlit run app.py
    ```
6. Open the browser link (usually http://localhost:8501) and ask questions.

## Features

- Local, free retrieval-augmented Q&A
- Math calculation tool
- Decision logging
