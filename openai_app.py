import streamlit as st
from openai import OpenAI

st.title('GenAI App')
st.header('Code Reviewer')

# Read API key from a file
with open('app_key.txt') as f:
    OPENAI_API_KEY = f.read().strip()

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to handle API call with retry logic
def make_api_call(query):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "analyze the submitted code and identify potential bugs, errors, or areas of improvement"},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error("An error occurred while processing your request.")
        st.error(str(e))
        return None

# User input
query = st.text_area('Paste your code here: ')

# Submit button
if st.button('Review Code'):
    response = make_api_call(query)
    if response:
        st.write(response)
