from flask import Flask, render_template, request, redirect, url_for
import requests
from PIL import Image, ImageTk
import io
import mysql.connector
from mysql.connector import Error
import uuid
import subprocess

app = Flask(__name__)

# Function to create database connection
def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host='sql6.freesqldatabase.com',
            database='sql6686488',
            user='sql6686488',
            password='JQEXrIGUzH')
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Function to create a new voter in the database
def create_voter(uid, age, city, connection):
    try:
        cursor = connection.cursor()
        unique_id = str(uuid.uuid4())
        query = "update citizens set DVID = (%s) where UID = (%s)"
        cursor.execute(query, (unique_id, uid))
        connection.commit()
        return f"Voter registered successfully with ID: {unique_id}"
    except Error as e:
        return f"Failed to insert record into MySQL table: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to run the second script
def run_second_script():
    second_script_path = "D:/PROJECTS/PROJECTS/EvmX/HackWithMait/guic.py"
    subprocess.Popen(["python", second_script_path])

# Download and set the logo
def set_logo(url, label):
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    pil_image = Image.open(image_bytes)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        connection = create_database_connection()
        if connection:
            message = create_voter(name, age, city, connection)
            return render_template("index.html", message=message)
        else:
            return render_template("index.html", message="Failed to connect to the database")
    return render_template("index.html")

@app.route("/vote")
def vote():
    run_second_script()
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Run the Flask app on custom port 8080
    app.run(debug=True, port=5005)