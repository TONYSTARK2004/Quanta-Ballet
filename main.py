import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import uuid

# Database connection function
def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='voters',
            user='root',
            password='PHW#84#jeor')
        return connection
    except Error as e:
        messagebox.showerror("Error", "Error while connecting to MySQL: " + str(e))
        return None

# Function to insert voter into the database
def create_voter(name, age, city, connection):
    try:
        cursor = connection.cursor()
        unique_id = str(uuid.uuid4())
        query = "INSERT INTO citizens (name, age, city, unique__id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, age, city, unique_id))
        connection.commit()
        messagebox.showinfo("Success", "Voter registered successfully with ID: " + unique_id)
    except Error as e:
        messagebox.showerror("Error", "Failed to insert record into MySQL table: " + str(e))
    finally:
        if connection.is_connected():
            cursor.close()

# Register Voter
def register_voter():
    name = name_entry.get()
    age = age_entry.get()
    city = city_entry.get()
    connection = create_database_connection()
    if connection is not None:
        create_voter(name, age, city, connection)
        connection.close()

# Create main window
root = tk.Tk()
root.title("Voter Registration System")

# Create and place widgets
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Age:").grid(row=1, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)

tk.Label(root, text="City:").grid(row=2, column=0)
city_entry = tk.Entry(root)
city_entry.grid(row=2, column=1)

submit_button = tk.Button(root, text="Register", command=register_voter)
submit_button.grid(row=3, column=0)

clear_button = tk.Button(root, text="Clear", command=lambda: [name_entry.delete(0, tk.END), age_entry.delete(0, tk.END), city_entry.delete(0, tk.END)])
clear_button.grid(row=3, column=1)

# Run the application
root.mainloop()
