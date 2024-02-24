from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host='sql6.freesqldatabase.com',
            database='sql6686488',
            user='sql6686488',
            password='JQEXrIGUzH')
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def get_citizen_with_unique_id(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM citizens WHERE DVID IS NOT NULL"
        cursor.execute(query)
        citizen = cursor.fetchone()
        cursor.close()  # Explicitly close cursor to avoid 'Unread result found' error
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
        # Insert the vote into the 'Voted' table
        count_query = "INSERT INTO Voted (UID, name) VALUES (%s, %s)"
        cursor.execute(count_query, (citizen_id, party_name))
        # Increment the vote count for the chosen party
        update_query = "UPDATE partie SET No_of_Votes = No_of_Votes + 1 WHERE name = %s"
        cursor.execute(update_query, (party_name,))
        # Delete the citizen with the given ID from the 'citizens' table
        delete_query = "DELETE FROM citizens WHERE DVID = %s"
        cursor.execute(delete_query, (citizen_id,))
        connection.commit()
        print("Vote recorded successfully for", party_name)
    except Error as e:
        print("Error updating votes or deleting citizen in MySQL tables", e)
        connection.rollback()  # Rollback changes in case of an error
    finally:
        if connection.is_connected():
            cursor.close()

@app.route('/')
def index():
    connection = create_database_connection()
    if connection:
        citizen = get_citizen_with_unique_id(connection)
        if citizen:
            citizen_info = f"Citizen found with ID: {citizen[0]} Having name: {citizen[1]}"
        else:
            citizen_info = "No eligible citizens found to vote."
        connection.close()
    else:
        citizen_info = "Failed to connect to the database"
    return render_template('index.html', citizen_info=citizen_info)

@app.route('/vote', methods=['POST'])
def vote():
    connection = create_database_connection()
    if connection:
        citizen = get_citizen_with_unique_id(connection)
        if citizen:
            party_name = request.form['party']
            # Check if the citizen has already voted
            if not has_already_voted(connection, citizen[0]):
                vote_and_delete_citizen(citizen[0], party_name, connection)
                return jsonify({'message': f"Vote recorded for {party_name}"})
            else:
                return jsonify({'message': "You have already voted."})
        else:
            return jsonify({'error': "No eligible citizens found to vote."})
        connection.close()
    else:
        return jsonify({'error': "Failed to connect to the database"})

def has_already_voted(connection, citizen_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Voted WHERE UID = %s"
        cursor.execute(query, (citizen_id,))
        return cursor.fetchone() is not None
    except Error as e:
        print("Error checking if citizen has already voted", e)
        return True  # Assume an error and prevent voting
    finally:
        if connection.is_connected():
            cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
