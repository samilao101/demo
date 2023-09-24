import streamlit as st
import os
import shutil
import random
import string

# Generate a random 4-digit number
random_number = ''.join(random.choices(string.digits, k=4))

# Your Python code


def code(name):
    python_code = f"""\
import streamlit as st

st.header("New Page: {name}")
"""
    return python_code

if st.button('Create Page'):
    file_name = f"Page_{random_number}.py"
    folder_name = "pages"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created '{folder_name}' folder.")

    file_path = os.path.join(folder_name, file_name)

    with open(file_path, "w") as file:
        file.write(code(file_name))

    print(f"Created '{file_name}' in the '{folder_name}' folder.")


