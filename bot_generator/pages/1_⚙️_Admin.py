import streamlit as st
from forms_templates.templates import generate_page_template
import os
import shutil
import random
import string
import openai
from io import StringIO
from dotenv import load_dotenv
import io
import sqlite3
from database import database_manager as db_manager


load_dotenv()
print(os.curdir)

db_manager.create_table()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

st.header("Create a Bot")

name = st.text_input("Name of Bot")

col1, col2 = st.columns(2)
formatted_response = ""


data = st.file_uploader("Instructions File", type=['txt'])


if st.button("Generate Purpose from File"):
    if data is not None:
        string_data = StringIO(data.getvalue().decode("utf-8"))
        gsar_prompt = f"summarize the following text into 4 sentences describing it in the way you would see it as introductory paragraph:  {string_data.read()} /n/n "
        
        with st.spinner("Generating response..."):
            generated_response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {"role": "user", "content": gsar_prompt}
                ],
                temperature=0.0
            )

            formatted_response = generated_response['choices'][0]['message']['content']

purpose = st.text_area("Purpose of Bot", formatted_response)


if data is not None and purpose is not "" and name is not "":
    if st.button("Create"):
        file_name = f"{name}.py"
        folder_name = "pages"

        if data is not None:
            try:
                file_extension = os.path.splitext(data.name)[-1].lower()
                    
                # Specify the folder where you want to save the file
                save_folder = "dataform"
                    
                    # Create the folder if it doesn't exist
                if not os.path.exists(save_folder):
                        os.makedirs(save_folder)
                    
                    # Construct the full path to save the file
                save_path = os.path.join(save_folder, data.name)
                    
                    # Save the file to the specified location
                with open(save_path, "wb") as f:
                    f.write(data.read())

                st.success(f"File '{data.name}' saved to {save_path}")

            except Exception as e:
                st.error(f"Error saving file: {e}")
            
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            st.write(f"Created '{folder_name}' folder.")

        file_path = os.path.join(folder_name, file_name)

        try:
            with open(file_path, "w") as file:
                file.write(generate_page_template(name, data.name, purpose))

            st.success(f"Created '{file_name}' in the '{folder_name}' folder.")

            db_manager.create_bot(name, purpose, data)
            name = None
            purpose = None


        except Exception as e:
            st.error(f"Error creating bot script: {e}")


bots_data = db_manager.get_all_bots()


st.divider()
if bots_data is not None:
    st.header("Built:")
    for bot in bots_data:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            new_name = st.text_input("Name", bot[1])

        with col2:
            new_purpose = st.text_area("Purpose", bot[2])

        with col3:
            new_data = st.file_uploader(f"{bot[3]}", type=['txt'])

        with col4:
            if st.button(f"Update {bot[1]}"):
                db_manager.update_bot(bot[0], new_name, new_purpose)

                if new_data is not None:
                    db_manager.delete_bot_file(f"dataform/{bot[3]}")
                    db_manager.create_new_file(new_data)
                    db_manager.update_bot_file_db(bot[0], new_data.name)



        with col5:
            if st.button(f"Delete {bot[1]}", type="primary"):
                print("updating")




st.divider()
st.title('Delete All:')
st.write("Click the button below to delete all data from the database.")

# Button to delete data
if st.button('Delete All Data'):
    db_manager.delete_all()
    st.write("All data has been deleted from the database.")

