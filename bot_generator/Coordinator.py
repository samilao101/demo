
import streamlit as st
import os
import openai
from dotenv import load_dotenv
import io
from database import database_manager as db_manager
from forms_templates import prompt_generator

os.environ['REQUESTS_CA_BUNDLE'] = 'certificate\certificate.crt'


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


st.image("cumminslogo.png")
st.header("FAQ Process Finder:")

question = st.text_input(
    "Please type below what you would like to learn more about and I will try to find the process for you to ask your questions. ", placeholder="Enter question...")

formatted_response = ""


if st.button("Search") and question != "":
        prompt_question =  prompt_generator.generate_coordinator_prompt(question)
        with st.spinner("Generating response..."):
            generated_response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {"role": "user", "content": prompt_question}
                ],
                temperature=0.0
            )

            formatted_response = generated_response['choices'][0]['message']['content']


if formatted_response != "":
    print(formatted_response)
    st.markdown(formatted_response)
else:
    st.markdown(f"Provide context as what you are searching for and we might be able to find the right process bot for you.")