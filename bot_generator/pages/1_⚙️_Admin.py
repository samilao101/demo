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
import time
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

os.environ['REQUESTS_CA_BUNDLE'] = 'certificate\certificate.crt'


file_path = Path(__file__).parent.parent / "hashed_pw.pkl"

with open(file_path, "rb") as file:
    hashed_passwords = pickle.load(file)

# Define other user information
names = ["Humberto De La Cruz", "Peter Parker"]
usernames = ["qd990", "pp990"]
emails = ["humberto.de.la.cruz.santos", "parker@gmail.com"]

# Create a credentials dictionary with hashed passwords
credentials_dict = {
    'usernames': {},
}

# Populate the credentials dictionary with user information including hashed passwords
for username, name, email, hashed_password in zip(usernames, names, emails, hashed_passwords):
    credentials_dict['usernames'][username] = {
        'name': name,
        'email': email,
        'password': hashed_password,  # Use the loaded hashed password
    }

# Other parameters
cookie_name = 'jwt_cookie'
key = 'your_secret_key'
cookie_expiry_days = 30.0
preauthorized_users = ['user3@example.com', 'user4@example.com']  # List of preauthorized emails

# Create an instance of the Authenticate class with the credentials dictionary
authenticator = stauth.Authenticate(
    credentials=credentials_dict,
    cookie_name=cookie_name,
    key=key,
    cookie_expiry_days=cookie_expiry_days,
    preauthorized=preauthorized_users,
)

user_name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect.")

if authentication_status == None:
    st.warning("Please enter username and password.")

if authentication_status == True:
    load_dotenv()

    db_manager.create_table()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

    authenticator.logout(f"Logout {user_name}", "main")
    st.header("Create a Bot")

    if 'show_fields' not in st.session_state:
        st.session_state.show_fields = True

    if st.session_state.show_fields == True:
        name = st.text_input("Name of Bot")

        col1, col2 = st.columns(2)

        data = st.file_uploader("Instructions File", type=['txt'])

        if 'formatted_response' not in st.session_state:
            st.session_state.formatted_response = ""

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
                    st.session_state.formatted_response = formatted_response



        purpose = st.text_area("Purpose of Bot", st.session_state.formatted_response)




        if data is not None and purpose != "" and name != "":
            if st.button("Create"):
                file_name = f"{name}.py"
                folder_name = "pages"
                
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


                except Exception as e:
                    st.error(f"Error saving file: {e}")
                    
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                file_path = os.path.join(folder_name, file_name)

                try:
                    bot_id = db_manager.create_bot(name, purpose, data)
                    with open(file_path, "w") as file:
                        file.write(generate_page_template(name, data.name, purpose, bot_id))

                    st.success(f"Created Bot {name}.")

                    
                    st.session_state.show_fields = False

                    st.session_state.formatted_response = ""




                except Exception as e:
                    st.error(f"Error creating bot script: {e}")

    else:
        st.success(f"Created New Bot")
        if st.button("Add More"):
            st.session_state.show_fields = True





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
                    db_manager.update_file_name(f"pages/{bot[1]}.py", f"{new_name}.py")


                    if new_data is not None:
                        db_manager.delete_bot_file(f"dataform/{bot[3]}")
                        db_manager.create_new_file(new_data)
                        db_manager.update_bot_file_db(bot[0], new_data.name)



            with col5:
                if st.button(f"Delete {bot[1]}", type="primary"):
                    db_manager.delete_row_by_id(bot[0])
                    db_manager.delete_bot_file(f"pages/{bot[1]}.py")
            st.divider()




    st.divider()
    st.title('Delete All:')
    st.write("Click the button below to delete all data from the database.")

    # Button to delete data
    if st.button('Delete All Data'):
        db_manager.delete_all_files()
        db_manager.delete_all_bots_from_db()

        st.write("All data has been deleted from the database.")

