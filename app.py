import base64
from ui import get_css  
import asyncio
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig, chain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredFileLoader
import logging


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


load_dotenv()
logging.basicConfig(level=logging.INFO)


ASSISTANT_AVATAR = "images/avatar.png" 



try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.6)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
except Exception as e:
    st.error(f"Error initializing Google AI models: {e}. Check your GOOGLE_API_KEY.")
    st.stop()


# rag document processing 
@st.cache_resource(show_spinner="Processing documents...")
def create_vectorstore_from_files(_uploaded_files):
    logging.info("--- CREATING NEW VECTOR STORE ---")
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    all_chunks = []

    for file in _uploaded_files:
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer)
        
        try:
            loader = UnstructuredFileLoader(file_path)
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_documents(docs)
            all_chunks.extend(chunks)
            logging.info(f"Successfully processed {file.name}")
        except Exception as e:
            logging.error(f"Error processing file {file.name}: {e}. Skipping this file.")
            st.warning(f"Could not process file: {file.name}. Skipping.")

    if not all_chunks:
        logging.warning("No processable content found in any of the files.")
        return None

    logging.info(f"Creating FAISS vector store from {len(all_chunks)} chunks...")
    vectorstore = FAISS.from_documents(documents=all_chunks, embedding=embeddings)
    logging.info("--- VECTOR STORE CREATED AND CACHED ---")
    return vectorstore.as_retriever()



def get_conversational_rag_chain(retriever):
    rephrase_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant. Given the chat history and a follow-up question, rephrase the follow-up question to be a standalone question."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])
    
    question_rephraser_chain = (rephrase_prompt | llm | StrOutputParser())

    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert assistant. Answer the user's question based ONLY on the following context derived from the documents:\n\n<context>{context}</context>\n\nIf the answer is not in the context, state you do not have that information from the provided documents."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])
    
    @chain
    def rephrase_and_retrieve(input_dict):
        config = RunnableConfig(callbacks=input_dict.get("callbacks")) 
        rephrased_question = question_rephraser_chain.invoke(input_dict, config)
        docs = retriever.invoke(rephrased_question, config)
        return {
            "context": "\n\n".join(doc.page_content for doc in docs),
            "chat_history": input_dict["chat_history"],
            "input": input_dict["input"]
        }
    return rephrase_and_retrieve | answer_prompt | llm | StrOutputParser()


def get_general_chat_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Answer the user's questions clearly and concisely."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])
    return prompt | llm | StrOutputParser()



st.set_page_config(
    layout="wide",
    page_title="Multi-Mode Chatbot", 
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# --- CHANGED: Call get_css without the background image parameter ---
st.markdown(get_css(), unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = {"Chatbot": [], "RAG": []}
if "vector_store_retriever" not in st.session_state:
    st.session_state.vector_store_retriever = None


with st.sidebar:
    st.header("Chat Mode")
    chat_mode = st.radio(
        "Choose your chat mode:",
        ("General Chatbot", "Chat with Your Docs"),
        key="chat_mode"
    )

    if chat_mode == "Chat with Your Docs":
        st.info("Upload one or more documents (PDF, DOCX, TXT) and ask questions about them.")
        uploaded_files = st.file_uploader(
            "Upload your files", 
            accept_multiple_files=True, 
            type=["pdf", "docx", "txt"]
        )
        
        if uploaded_files:
            st.session_state.vector_store_retriever = create_vectorstore_from_files(tuple(uploaded_files))
            if "docs_processed" not in st.session_state:
                 st.success("Documents processed!")
                 st.session_state.docs_processed = True
        elif not st.session_state.vector_store_retriever:
             st.warning("Please upload at least one document to start RAG chat.")
    else:
        st.info("This is a general-purpose chatbot. It will not use any uploaded documents.")
        st.session_state.docs_processed = False

    st.divider()
    
    history_key = "RAG" if chat_mode == "Chat with Your Docs" else "Chatbot"
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages[history_key] = []
        logging.info(f"Chat history for {history_key} cleared.")
        st.rerun()


if chat_mode == "General Chatbot":
    st.title("Gemini Bot")
    st.markdown("Ask me anything! I'm here to help with general questions.")
else:
    st.title("Doc Bot")
    st.markdown("Upload documents in the sidebar and I'll answer specific questions about them.")



active_history = st.session_state.messages[history_key]

for msg in active_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user", avatar = "🙋🏻").markdown(msg.content)
    elif isinstance(msg, AIMessage):

        st.chat_message("assistant", avatar=ASSISTANT_AVATAR).markdown(msg.content)

user_prompt = st.chat_input("What would you like to ask?")

if user_prompt:
    active_history.append(HumanMessage(content=user_prompt))
    st.chat_message("user",avatar = "🙋🏻").markdown(user_prompt)


    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        with st.spinner("Thinking..."):
            
            if chat_mode == "General Chatbot":
                chat_chain = get_general_chat_chain()
                input_data = {"input": user_prompt, "chat_history": active_history}
                response_stream = chat_chain.stream(input_data)
                assistant_reply = st.write_stream(response_stream)
                
            elif chat_mode == "Chat with Your Docs":
                if st.session_state.vector_store_retriever is not None:
                    rag_chain = get_conversational_rag_chain(st.session_state.vector_store_retriever)
                    input_data = {"input": user_prompt, "chat_history": active_history}
                    response_stream = rag_chain.stream(input_data)
                    assistant_reply = st.write_stream(response_stream)
                else:
                    assistant_reply = "Please upload one or more documents in the sidebar before asking questions in this mode."
                    st.markdown(assistant_reply)

            active_history.append(AIMessage(content=assistant_reply))