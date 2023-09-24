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


load_dotenv()


connection = sqlite3.connect('bot_database.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bots (id INTEGER PRIMARY KEY, bot_name TEXT, bot_purpose TEXT, bot_file_name TEXT)''')


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

st.header("Create a Bot")

name = st.text_input("Name of Bot")

data = st.file_uploader("Instructions", type=['txt'])

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


    clicked = st.button("Create")

    if clicked:
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

            cursor.execute('''INSERT INTO bots (bot_name, bot_purpose, bot_file_name) VALUES (?, ?, ?)''', (name,purpose,data.name))

            # Commit the changes to the database
            connection.commit()
        except Exception as e:
            st.error(f"Error creating bot script: {e}")

connection = sqlite3.connect('bot_database.db')
cursor = connection.cursor()
cursor.execute('''SELECT * FROM bots''')
bots_data = cursor.fetchall()
connection.close()
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
                print("updating")

        with col5:
            if st.button(f"Delete {bot[1]}", type="primary"):
                print("updating")

connection = sqlite3.connect('mydatabase.db')
cursor = connection.cursor()

# Streamlit app title and description
st.divider()
st.title('Delete All:')
st.write("Click the button below to delete all data from the database.")

# Button to delete data
if st.button('Delete All Data'):
    # Execute the DELETE statement to remove all data
    cursor.execute('''DELETE FROM bots''')
    
    # Commit the changes to the database
    connection.commit()

    # Inform the user that data has been deleted
    st.write("All data has been deleted from the database.")

# Close the database connection
connection.close()