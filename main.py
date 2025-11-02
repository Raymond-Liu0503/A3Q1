# Raymond Liu 101264487
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

from sqlalchemy import create_engine

import os

DATABASE_URL = os.environ.get("POSTGRES_URL")
if not DATABASE_URL:
    raise RuntimeError("Missing DATABASE_URL environment variable")

import socket
hostname = socket.gethostbyname(socket.gethostname())
engine = create_engine(DATABASE_URL, future=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Student(Base):
    '''Student model representing a student record'''
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    enrollment_date = Column(Date)

def getAllStudents():
    '''Retrieve all student records from the database'''
    session = Session()
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, Email: {student.email}, Enrollment Date: {student.enrollment_date}")
    session.close()
    return students

def addStudent(first_name, last_name, email, enrollment_date=date.today()):
    '''Add a new student record to the database'''
    session = Session()
    new_student = Student(first_name=first_name, last_name=last_name, email=email, enrollment_date=enrollment_date)
    session.add(new_student)
    session.commit()
    print(f"Added student: {first_name} {last_name}")
    session.close()

def updateStudent(student_id, first_name=None, last_name=None, email=None, enrollment_date=None):
    '''Update an existing student record in the database'''
    session = Session()
    student = session.query(Student).filter_by(student_id=student_id).first()
    if student:
        if first_name:
            student.first_name = first_name
        if last_name:
            student.last_name = last_name
        if email:
            student.email = email
        if enrollment_date:
            student.enrollment_date = enrollment_date
        session.commit()
        print(f"Updated student ID: {student_id}")
    else:
        print(f"Student ID: {student_id} not found")
    session.close()

def deleteStudent(student_id):
    '''Delete a student record from the database'''
    session = Session()
    student = session.query(Student).filter_by(student_id=student_id).first()
    if student:
        session.delete(student)
        session.commit()
        print(f"Deleted student ID: {student_id}")
    else:
        print(f"Student ID: {student_id} not found")
    session.close()

if __name__ == "__main__":
    option = input("Choose an option: 1) View Students 2) Add Student 3) Update Student 4) Delete Student\n")
    if option == '1':
        getAllStudents()
    elif option == '2':
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        addStudent(first_name, last_name, email)
    elif option == '3':
        student_id = int(input("Student ID to update: "))
        first_name = input("New First Name (leave blank to keep current): ")
        last_name = input("New Last Name (leave blank to keep current): ")
        email = input("New Email (leave blank to keep current): ")
        updateStudent(student_id, first_name or None, last_name or None, email or None)
    elif option == '4':
        student_id = int(input("Student ID to delete: "))
        deleteStudent(student_id)
    else:
        print("Invalid option")