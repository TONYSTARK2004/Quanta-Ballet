import mysql.connector
from mysql.connector import Error

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

def cast_vote(unique_id, candidate, connection):
    try:
        cursor = connection.cursor()
        # Check if the unique_id is valid and not already used for voting
        query = "SELECT * FROM voters WHERE unique_id = %s AND has_voted = FALSE"
        cursor.execute(query, (unique_id,))
        if cursor.fetchone() is not None:
            # Update the vote
            update_query = "UPDATE voters SET has_voted = TRUE, voted_for = %s WHERE unique_id = %s"
            cursor.execute(update_query, (candidate, unique_id))
            connection.commit()
            print("Vote cast successfully for candidate:", candidate)
        else:
            print("Invalid ID or vote already cast.")
    except Error as e:
        print("Failed to cast vote", e)
    finally:
        if connection.is_connected():
            cursor.close()

def main():
    # Establish database connection
    connection = create_database_connection()

    if connection is not None:
        # Input voter's unique ID and candidate choice
        unique_id = input("Enter your unique voter ID: ")
        candidate = input("Enter the name of the candidate you wish to vote for: ")

        # Cast the vote
        cast_vote(unique_id, candidate, connection)

        # Close the connection
        connection.close()
    else:
        print("Failed to connect to the database")

if __name__ == "__main__":
    main()
