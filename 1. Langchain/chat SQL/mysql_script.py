import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        user='root',
        password=''
    )

    if connection.is_connected():
        print("Connected to MySQL server")
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS STUDENTS")
        cursor.execute("USE STUDENTS")

        table_info = """
        CREATE TABLE IF NOT EXISTS STUDENT (
            NAME VARCHAR(50),
            CLASS VARCHAR(10),
            SECTION VARCHAR(5),
            MARKS INT,
            ROLLNO INT PRIMARY KEY,
            EMAIL VARCHAR(50),
            PHONE VARCHAR(15),
            ADDRESS VARCHAR(100)
        )
        """
        cursor.execute(table_info)
        print("Table created")

        # List of records to insert
        records = [
            ('Ananya Sharma', '10', 'A', 88, 1001, 'ananya.sharma@email.com', '9876543210', '123 Main St, Delhi'),
            ('Ravi Kumar', '10', 'B', 76, 1002, 'ravi.kumar@email.com', '9876543211', '45 Nehru Nagar, Patna'),
            ('Priya Mehta', '9', 'A', 92, 1003, 'priya.mehta@email.com', '9876543212', '12 Park Lane, Jaipur'),
            ('Aman Verma', '9', 'C', 64, 1004, 'aman.verma@email.com', '9876543213', '88 Gandhi Rd, Lucknow'),
            ('Sneha Gupta', '8', 'B', 81, 1005, 'sneha.gupta@email.com', '9876543214', '31 Civil Lines, Kanpur'),
            ('Kunal Joshi', '8', 'A', 73, 1006, 'kunal.joshi@email.com', '9876543215', '77 Model Town, Amritsar'),
            ('Ritika Singh', '7', 'C', 85, 1007, 'ritika.singh@email.com', '9876543216', '90 Cross Rd, Mumbai'),
            ('Manish Yadav', '7', 'A', 67, 1008, 'manish.yadav@email.com', '9876543217', '23 East End, Noida'),
            ('Divya Nair', '6', 'B', 90, 1009, 'divya.nair@email.com', '9876543218', '11 MG Road, Kochi'),
            ('Nikhil Rao', '6', 'C', 78, 1010, 'nikhil.rao@email.com', '9876543219', '39 Hilltop, Bangalore'),
            ('Isha Jain', '5', 'A', 84, 1011, 'isha.jain@email.com', '9876543220', '80 Rajpath, Ahmedabad'),
            ('Arjun Das', '5', 'B', 59, 1012, 'arjun.das@email.com', '9876543221', '59 Cantonment, Ranchi'),
            ('Neha Reddy', '4', 'C', 88, 1013, 'neha.reddy@email.com', '9876543222', '100 South City, Hyderabad'),
            ('Rohit Malhotra', '4', 'A', 72, 1014, 'rohit.malhotra@email.com', '9876543223', '7 West Street, Ludhiana'),
            ('Meena Iyer', '3', 'B', 95, 1015, 'meena.iyer@email.com', '9876543224', '33 Station Rd, Chennai'),
            ('Sameer Khan', '10', 'C', 89, 1016, 'sameer.khan@email.com', '9876543225', '22 River View, Bhopal'),
            ('Laxmi Tripathi', '9', 'B', 91, 1017, 'laxmi.tripathi@email.com', '9876543226', '66 Garden Lane, Indore'),
            ('Jatin Mehra', '8', 'C', 65, 1018, 'jatin.mehra@email.com', '9876543227', '41 College Rd, Nashik'),
            ('Tanya Dutt', '7', 'B', 83, 1019, 'tanya.dutt@email.com', '9876543228', '15 Circular Rd, Pune'),
            ('Aarav Chawla', '6', 'A', 74, 1020, 'aarav.chawla@email.com', '9876543229', '5 Tech Park, Surat'),
        ]

        insert_query = """
        INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, ROLLNO, EMAIL, PHONE, ADDRESS)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(insert_query, records)
        connection.commit()
        print(f"{cursor.rowcount} records inserted.")

        # Fetching and displaying data
        cursor.execute("SELECT * FROM STUDENT")
        result = cursor.fetchall()
        for row in result:
            print(row)

except Error as e:
    print(f"Error occurred: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
