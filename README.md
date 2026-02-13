# Gemini RAG Chatbot

This project is a fully functional RAG chatbot built using the Google Gemini Pro API and a local ChromaDB vector store. 
The interface is created with Streamlit.

The chatbot allows you to "chat" with your own custom documents. It first populates a vector database from text files and then uses the Gemini LLM to generate answers to your questions based *only* on the context found in those documents.



## Features

* **RAG Pipeline:** Implements a complete Retrieval-Augmented Generation workflow.
* **Vector Store:** Uses `ChromaDB` to store vector embeddings locally.
* **Document Population:** Includes a script (`populate_db.py`) to process source documents and populate the vector store.
* **Web Interface:** A clean, easy-to-use chat interface built with `Streamlit`.
* **LLM Integration:** Powered by the Google Gemini Pro API for high-quality text generation.

## Tech Stack

* **Language:** Python 3
* **LLM:** Google Gemini Pro
* **Framework:** Streamlit
* **Vector Database:** ChromaDB
* **Embeddings:** GoogleGenerativeAIEmbeddings

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/TanujaNair03/gemini-rag-chatbot.git](https://github.com/TanujaNair03/gemini-rag-chatbot.git)
cd gemini-rag-chatbot
