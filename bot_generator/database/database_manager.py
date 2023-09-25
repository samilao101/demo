import sqlite3
import os

database_location = "database/bot_database.db"

def create_table():
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bots (id INTEGER PRIMARY KEY, bot_name TEXT, bot_purpose TEXT, bot_file_name TEXT)''')
    connection.commit()
    connection.close()

def create_bot(name, purpose, data):
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO bots (bot_name, bot_purpose, bot_file_name) VALUES (?, ?, ?)''', (name,purpose,data.name))
    print("created bot")
    connection.commit()
    connection.close()

def get_all_bots():
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM bots''')
    bots_data = cursor.fetchall()
    connection.close()
    return bots_data

def delete_all():
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()
    cursor.execute('''DELETE FROM bots''')
    connection.commit()
    connection.close()


def update_bot(update_id, new_name, new_purpose):
    connection = sqlite3.connect(database_location)

    # Create a cursor object
    cursor = connection.cursor()

    # Construct the SQL update query with placeholders
    sql_update = "UPDATE bots SET bot_name = ?, bot_purpose = ? WHERE id = ?"

    # Provide values as a tuple in the second argument of execute
    cursor.execute(sql_update, (new_name, new_purpose, update_id))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()


def delete_bot_file(existing_file_path):
    if os.path.exists(existing_file_path):
        try:
            # Delete the file
            os.remove(existing_file_path)
            print(f"File '{existing_file_path}' has been deleted.")

        except OSError as e:
            print(f"Error: {e}")
    else:
        print(f"File '{existing_file_path}' does not exist.")

def create_new_file(new_file):
    try:
        file_extension = os.path.splitext(new_file.name)[-1].lower()
                
        # Specify the folder where you want to save the file
        save_folder = "dataform"
                
                # Construct the full path to save the file
        save_path = os.path.join(save_folder, new_file.name)
                
                # Save the file to the specified location
        with open(save_path, "wb") as f:
            f.write(new_file.read())

    except Exception as e:
        print(f"Error saving file: {e}")


def update_bot_file_db(update_id, new_file_name):
    conn = sqlite3.connect(database_location)

    # Create a cursor object
    cursor = conn.cursor()

    # Construct the SQL update query with placeholders
    sql_update = "UPDATE bots SET bot_file_name = ? WHERE id = ?"

    # Provide values as a tuple in the second argument of execute
    cursor.execute(sql_update, (new_file_name, update_id))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
