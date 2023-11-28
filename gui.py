import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
import mysql.connector
from mysql.connector import Error
import uuid

# Function to create database connection
def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='voters',
            user='root',
            password='PHW#84#jeor')
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Function to create a new voter in the database
def create_voter(name, age, city, connection):
    try:
        cursor = connection.cursor()
        unique_id = str(uuid.uuid4())
        query = "update citizens set Unique__id = (%s) where Name = (%s)"
        cursor.execute(query, (unique_id, name))
        connection.commit()
        return f"Voter registered successfully with ID: {unique_id}"
    except Error as e:
        return f"Failed to insert record into MySQL table: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to handle the submit button click
def on_submit():
    name = name_entry.get()
    age = age_entry.get()
    city = city_entry.get()

    connection = create_database_connection()
    if connection:
        message = create_voter(name, age, city, connection)
        result_label.config(text=message)
    else:
        result_label.config(text="Failed to connect to the database")

# Download and set the logo
def set_logo(url, label):
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    pil_image = Image.open(image_bytes)
    tk_image = ImageTk.PhotoImage(pil_image)
    label.config(image=tk_image)
    label.image = tk_image

# Create the main window
root = tk.Tk()
root.title("Voter Registration")

# Logo
logo_url = "https://images.freeimages.com/cme/images/previews/047/national-emblem-of-india-satyamev-jayate-vector-25883.jpg"
logo_label = tk.Label(root)
logo_label.pack()
set_logo(logo_url, logo_label)

# Input fields and labels
name_label = tk.Label(root, text="Enter your name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

age_label = tk.Label(root, text="Enter your age:")
age_label.pack()
age_entry = tk.Entry(root)
age_entry.pack()

city_label = tk.Label(root, text="Enter your city:")
city_label.pack()
city_entry = tk.Entry(root)
city_entry.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

# Result label
result_label = tk.Label(root, text="")
result_label.pack()

# Run the application
root.mainloop()
