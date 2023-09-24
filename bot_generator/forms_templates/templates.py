def  generate_page_template(bot_name, document_path, definition):
    template = f"""
import streamlit as st
import os
import openai
from dotenv import load_dotenv
import io

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

file_path = 'dataform/{document_path}'

with open(file_path, 'r') as file:
    file_content = file.read()

st.image("cumminslogo.png")
st.header("{bot_name}")

prompt = st.text_input(
    "Please type your GSAR questions below. Questions/Responses may be monitored.", placeholder="Enter prompt...")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "char_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if prompt:
    gsar_prompt = f"Use the following context below to answer question:  {{prompt}} /n/n (Please use markdown to make the response easier to read). Do not make up answers and only respond to questions relevant to to the context. /n/n context: {{file_content}}"
    print(gsar_prompt)
    with st.spinner("Generating response..."):
        generated_response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {{"role": "user", "content": gsar_prompt}}
            ],
            temperature=0.0
        )

        formatted_response = generated_response['choices'][0]['message']['content']

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
        st.write(generated_response)
else:
    st.markdown("{definition}")
"""
    return template