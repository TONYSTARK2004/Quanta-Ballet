import mysql.connector
from mysql.connector import Error
import uuid

def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Or your MySQL server host
            database='voting_db',   # Your database name
            user='username',        # Your MySQL username
            password='password')    # Your MySQL password
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def create_voter(name, age, city, connection):
    try:
        cursor = connection.cursor()
        unique_id = str(uuid.uuid4())  # Generate a unique ID
        query = "INSERT INTO voters (name, age, city, unique_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, age, city, unique_id))
        connection.commit()
        print("Voter registered successfully with ID:", unique_id)
        # canbe sent to the user via email or SMS.
    except Error as e:
        print("Failed to insert record into MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
def main():
    # Establish database connection
    connection = create_database_connection()

    if connection is not None:
        # Input user data
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        city = input("Enter your city: ")

        # Create new voter
        create_voter(name, age, city, connection)

        # Close the connection
        connection.close()
    else:
        print("Failed to connect to the database")

if __name__ == "__main__":
    main()
