import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load the embedding model
embedding_model = GoogleGenerativeAIEmbeddings(google_api_key="AIzaSyBXNaFfHkldugJkMgvUjxGPHHcKZc7VLiM", 
                                               model="models/embedding-001")

# Setting a Connection with the ChromaDB
db_connection = Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)

# Define retrieval function to format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) 

# Converting CHROMA db_connection to Retriever Object
retriever = db_connection.as_retriever(search_kwargs={"k": 5})

# Define chat prompt template
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="""🤖 Welcome! I'm your helpful AI Bot. 
    I'm here to assist you based on the context you provide. 
    Let's make sure our conversation is both relevant and helpful."""),
    HumanMessagePromptTemplate.from_template("Please answer the question based on the given context.\nContext:\n{context}\nQuestion:\n{question}\nAnswer:")
])

# Initialize chat model
chat_model = ChatGoogleGenerativeAI(google_api_key="AIzaSyBXNaFfHkldugJkMgvUjxGPHHcKZc7VLiM", 
                                    model="gemini-1.5-pro-latest")

# Initialize output parser
output_parser = StrOutputParser()

# Define RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | chat_template
    | chat_model
    | output_parser
)
# Streamlit UI
st.title("👾 AI Rag ChatBot 👾")
st.subheader("An AI System for Contextual Question Answering based on the 'Leave No Context Behind' Paper")

question = st.text_input("Ask me anything:")

if st.button("🚀 Get Answer"):
    if question:
        response = rag_chain.invoke(question)
        st.write("💬 Answer:")
        st.write(response)
    else:
        st.warning("⚠️ Please enter a question.")

