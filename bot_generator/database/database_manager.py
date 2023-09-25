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
    bot_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return bot_id  # Return the ID of the inserted row


def get_all_bots():
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM bots''')
    bots_data = cursor.fetchall()
    connection.close()
    return bots_data

def delete_all_bots_from_db():
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


def get_bot_by_id(bot_id):
    connection = sqlite3.connect(database_location)
    cursor = connection.cursor()
    
    # Execute a SQL query to retrieve the bot by its ID
    cursor.execute('''SELECT * FROM bots WHERE id = ?''', (bot_id,))
    
    # Fetch the result (the first row matching the ID)
    bot = cursor.fetchone()
    
    connection.close()
    
    return bot  # Return the bot information as a tuple (or None if not found)

def update_file_name(old_file_path, new_file_name):
    # Extract the directory path from the old file path
    directory_path = os.path.dirname(old_file_path)
    
    # Construct the new file path with the updated name
    new_file_path = os.path.join(directory_path, new_file_name)
    
    try:
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"File name updated to: {new_file_name}")
        return new_file_path  # Return the new file path
    except OSError as e:
        print(f"Error updating file name: {e}")
        return None
    
def delete_row_by_id(row_id):
    try:
        connection = sqlite3.connect(database_location)
        cursor = connection.cursor()
        
        # Define the DELETE statement with a WHERE clause
        delete_query = f"DELETE FROM bots WHERE id = ?"
        
        # Execute the DELETE statement with the row_id as a parameter
        cursor.execute(delete_query, (row_id,))
        
        # Commit the changes to the database
        connection.commit()
        
        print(f"Row with ID {row_id} deleted successfully from bots.")
        
    except sqlite3.Error as e:
        print(f"Error deleting row: {e}")
    finally:
        # Close the database connection
        connection.close()


def delete_all_files():
    try:
        connection = sqlite3.connect(database_location)
        cursor = connection.cursor()

        # Fetch all bot records from the database
        cursor.execute('''SELECT * FROM bots''')
        bots = cursor.fetchall()

        for bot in bots:
            bot_id, bot_name, bot_purpose, bot_file_name = bot

            # Construct paths for the files to delete
            page_file_path = f"pages/{bot_name}.py"
            data_file_path = f"dataform/{bot_file_name}"

            # Verify that the files exist before attempting to delete them
            if os.path.exists(page_file_path):
                os.remove(page_file_path)
                print(f"Deleted page file: {page_file_path}")
            
            if os.path.exists(data_file_path):
                os.remove(data_file_path)
                print(f"Deleted data file: {data_file_path}")

        # Commit changes to the database
        connection.commit()
        connection.close()

    except sqlite3.Error as sqlite_error:
        print(f"SQLite error: {sqlite_error}")
    except OSError as os_error:
        print(f"OS error: {os_error}")

