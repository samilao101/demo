import pickle
from pathlib import Path 
import streamlit_authenticator as stauth

names = ["Humberto De La Cruz", "Peter Parker"]
usernames = ["qd990", "pp990"]
passwords = ["123abc", "456abc"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
