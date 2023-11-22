import mysql.connector
from mysql.connector import Error

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
        query = "SELECT * FROM citizens WHERE Unique__id IS NOT NULL "
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

def main():
    # Establish database connection
    connection = create_database_connection()

    if connection is not None:
        # Get a citizen with a non-null unique ID
        citizen = get_citizen_with_unique_id(connection)

        if citizen:
            cursor = connection.cursor()
            print("Citizen found with ID:", citizen[0])
            party_name = input("Enter the party you want to vote for: ")
            # Counting collected voters
            count_query = "INSERT INTO Voted VALUES (%s)"
            cursor.execute(count_query,(citizen[0],))

            # Record the vote and delete the citizen
            vote_and_delete_citizen(citizen[3], party_name, connection)
        else:
            print("No eligible citizens found to vote.")
        
        # Close the connection
        connection.close()
    else:
        print("Failed to connect to the database")

if __name__ == "__main__":
    main()
