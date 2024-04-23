import streamlit as st
import google.generativeai as genai
import openai

# Title and subtitle
st.title('DataNinja')
st.markdown("### :computer:")

# Load API key from file
with open(r"C:\Users\seeth\Desktop\python class\internship-2024\Gemini ai-chat bot\Gemini ai-api key.txt", "r") as f:
    api_key = f.read().strip()

# Configure OpenAI API
openai.api_key = api_key

# Initialize chat history if not already present
if "memory" not in st.session_state:
    st.session_state["memory"] = []

# Chitti chat interface
st.header("Robot is Ready to Assist You!")

# Configure GenerativeAI
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="""Hi! I'm ChittiRobot, your AI assistant for Data Science. I'm here to help you. Feel free to ask me anything related to Data Science or for assistance with any coding challenges you're facing. If the question is not related to data science, please note that I may not be able to provide the assistance you need."""
)

# Initialize chat history if not already present
if "memory" not in st.session_state:
    st.session_state["memory"] = []

# Start chat with the AI model
chat = model.start_chat(history=st.session_state["memory"])
st.chat_message("AI-chittirobot").write("Hi there! 👋 How can I help you today? 😊")

for message in chat.history:
    sender = "AI-chittirobot" if message.role == "model" else message.role
    st.chat_message(sender).write(message.parts[0].text)


user_input = st.chat_input()

if user_input:
    st.chat_message("user👤").write(user_input)
    response = chat.send_message(user_input)
    AC=st.chat_message("AI-chittirobot🤖").write(bot.text for bot in response)
    st.session_state["memory"] = chat.history



