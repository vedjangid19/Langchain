
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

table_info = """
Create table if not exists STUDENT(
NAME VARCHAR(25),
CLASS VARCHAR(25),
SECTION VARCHAR(25),
MARKS INT
)
"""

cursor.execute(table_info)

insert_records = """
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Ananya Sharma', '10', 'A', 88);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Ravi Kumar', '10', 'B', 76);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Priya Mehta', '9', 'A', 92);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Aman Verma', '9', 'C', 64);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Sneha Gupta', '8', 'B', 81);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Kunal Joshi', '8', 'A', 73);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Ritika Singh', '7', 'C', 85);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Manish Yadav', '7', 'A', 67);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Divya Nair', '6', 'B', 90);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Nikhil Rao', '6', 'C', 78);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Isha Jain', '5', 'A', 84);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Arjun Das', '5', 'B', 59);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Neha Reddy', '4', 'C', 88);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Rohit Malhotra', '4', 'A', 72);
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Meena Iyer', '3', 'B', 95);
"""

cursor.executescript(insert_records)

data = cursor.execute("SELECT * FROM STUDENT")

for record in data:
    print(record)

conn.commit()
conn.close()