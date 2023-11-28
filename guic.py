import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
import mysql.connector
from mysql.connector import Error

# Function to create database connection
def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='voters',
            user='root',
            password='PHW#84#jeor')
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def get_citizen_with_unique_id(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM citizens WHERE Unique__id IS NOT NULL"
        cursor.execute(query)
        citizen = cursor.fetchone()
        return citizen
    except Error as e:
        print("Error retrieving citizen from MySQL table", e)
        return None
    finally:
        if connection.is_connected():
            cursor.close()

def vote_and_delete_citizen(citizen_id, party_name, connection):
    try:
        cursor = connection.cursor()

        # Increment the vote count for the chosen party
        update_query = "UPDATE parties SET No_of_Votes = No_of_Votes + 1 WHERE Name = %s"
        cursor.execute(update_query, (party_name,))

        # Delete the citizen with the given ID
        delete_query = "DELETE FROM citizens WHERE Unique__id = %s"
        cursor.execute(delete_query, (citizen_id,))

        connection.commit()
        print("Vote recorded successfully for", party_name)
    except Error as e:
        print("Error updating votes or deleting citizen in MySQL tables", e)
    finally:
        if connection.is_connected():
            cursor.close()

def display_citizen_id():
    connection = create_database_connection()
    if connection:
        citizen = get_citizen_with_unique_id(connection)
        if citizen:
            citizen_id_label.config(text=f"Citizen found with ID: {citizen[0]}")
        else:
            citizen_id_label.config(text="No eligible citizens found to vote.")
        connection.close()

def on_vote():
    connection = create_database_connection()
    if connection:
        citizen = get_citizen_with_unique_id(connection)
        if citizen:
            party_name = party_entry.get()
            # Counting collected voters
            cursor = connection.cursor()
            count_query = "INSERT INTO Voted VALUES (%s)"
            cursor.execute(count_query, (citizen[0],))

            # Record the vote and delete the citizen
            vote_and_delete_citizen(citizen[3], party_name, connection)
            messagebox.showinfo("Success", f"Vote recorded for {party_name}")
        else:
            messagebox.showerror("Error", "No eligible citizens found to vote.")
        connection.close()
    else:
        messagebox.showerror("Error", "Failed to connect to the database")

def set_logo(url, label):
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    pil_image = Image.open(image_bytes)
    tk_image = ImageTk.PhotoImage(pil_image)
    label.config(image=tk_image)
    label.image = tk_image

root = tk.Tk()
root.title("Voting System")

# Logo
logo_url = "https://images.freeimages.com/cme/images/previews/047/national-emblem-of-india-satyamev-jayate-vector-25883.jpg"
logo_label = tk.Label(root)
logo_label.pack(side=tk.TOP)
set_logo(logo_url, logo_label)

# Citizen ID display
citizen_id_label = tk.Label(root, text="Fetching citizen ID...")
citizen_id_label.pack()

# Party voting input
party_label = tk.Label(root, text="Enter the party you want to vote for:")
party_label.pack()
party_entry = tk.Entry(root)
party_entry.pack()

# Vote button
vote_button = tk.Button(root, text="Vote", command=on_vote)
vote_button.pack()

# Display the citizen ID when the GUI starts
display_citizen_id()

root.mainloop()
