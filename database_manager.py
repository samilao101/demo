import sqlite3
import os

def update_bot(update_id, new_name, new_purpose):
    conn = sqlite3.connect("your_database.db")

    # 2. Create a cursor object
    cursor = conn.cursor()

    sql_update = f"UPDATE bots SET bot_name = {new_name}, bot_purpose = {new_purpose}, bot_file_name = {new_file_name} WHERE id = {update_id}"

    # 4. Execute the SQL statement
    cursor.execute(sql_update)

    # 5. Commit the changes to the database
    conn.commit()

    # 6. Close the cursor and the database connection
    cursor.close()
    conn.close()

def delete(existing_file_path):
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
    onn = sqlite3.connect("your_database.db")

    # 2. Create a cursor object
    cursor = conn.cursor()

    sql_update = f"UPDATE bots SET bot_file_name = {new_file_name} WHERE id = {update_id}"

    # 4. Execute the SQL statement
    cursor.execute(sql_update)

    # 5. Commit the changes to the database
    conn.commit()

    # 6. Close the cursor and the database connection
    cursor.close()
    conn.close()

