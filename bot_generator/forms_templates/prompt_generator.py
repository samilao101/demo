import sqlite3
from database import database_manager as db_manager
from streamlit_javascript import st_javascript


def convert_spaces_to_underscores_add_py(input_string):
    # Replace white spaces with underscores using the str.replace method
    result_string = input_string.replace(" ", "_")
    result_string = result_string + ".py"
    return result_string


def generate_coordinator_prompt(question):
    base_url = st_javascript("await fetch('').then(r => window.parent.location.href)")
    bots = db_manager.get_all_bots()
    processes = ""
    for bot in bots:
        bot_id, bot_name, bot_purpose, bot_file_name = bot
        processes = processes + f"[Process Name: {bot_name}, Definition: {bot_purpose}] "

    prompt = f"""
    Use the following question to determine which of the following processes more closely relate to the question based 
    on how closely matches its definition: \"{question}\".
    Processes to choose from:
    {processes}
    Return the process that more closely resembles the question with a response: Please use the following process: [<b>Process Name</b>.]
    Please only answer in that format with and converting the name into a link with base url: {base_url} and the process name having underscores instead of spaces. You can add an explanation why this process was selected.
    Do try your best to match it to an existing process, but if the question doesn't match any of the processes at all, say \' I was unable to find a related process, please use the following list of processes and definitions.' and provide all the processes and definitions and links in a nicely formatted markdown. 
    """
    return prompt



