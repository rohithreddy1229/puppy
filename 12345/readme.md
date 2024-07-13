
# Hospital Management System

## Overview
This Hospital Management System is designed to manage patients and doctors information using Python and MySQL.

## Table of Contents
- setup
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Using the Application](#using-the-application)
- [Queries and Reports](#queries-and-reports)

## Setup
1. **Install Dependencies:**
   Ensure you have Python and MySQL installed on your system.
   ```bash
   pip install mysql-connector-python
   ```

## Database Setup
1. **Create MySQL Database:**
   ```sql
   CREATE DATABASE HospitalDB;
   USE HospitalDB;
   ```

2. **Create Tables:**
   ```sql
   CREATE TABLE Doctors (
       doctor_id INT PRIMARY KEY,
       name VARCHAR(100),
       specialization VARCHAR(100)
   );

   CREATE TABLE Patients (
       patient_id INT PRIMARY KEY,
       name VARCHAR(100),
       age INT,
       gender VARCHAR(10),
       disease VARCHAR(100),
       doctor_id INT,
       FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
   );
   ```

## Running the Application
1. **Modify Database Connection:**
   Open `hospital_management_system.py` and update the MySQL connection details:
   ```python
   host='localhost',
   database='HospitalDB',
   user='your_username',
   password='your_password'
   ```

2. **Run the Application:**
   ```bash
   python hospital_management_system.py
   ```

## Using the Application
1. **Menu Options:**
   - **Add Patient**: Enter patient details to add a new patient to the database.
   - **Update Patient**: Update details of an existing patient.
   - **Delete Patient**: Remove a patient from the database.
   - **Add Doctor**: Enter doctor details to add a new doctor to the database.
   - **Update Doctor**: Update details of an existing doctor.
   - **Assign Doctor to Patient**: Assign a doctor to a specific patient.
   - **Generate Patient Report by Doctor**: Retrieve a list of patients assigned to a specific doctor.

2. **Input Format:**
   - Follow the prompts and enter data as requested (e.g., patient ID, name, age, gender, disease).

## Queries and Reports
1. **Total Number of Patients Assigned to Each Doctor:**
   ```sql
   SELECT doctor_id, COUNT(*) AS total_patients
   FROM Patients
   GROUP BY doctor_id;
   ```

2. **Names of Doctors and Total Number of Patients Assigned:**
   ```sql
   SELECT d.name AS doctor_name, COUNT(p.patient_id) AS total_patients
   FROM Doctors d
   LEFT JOIN Patients p ON d.doctor_id = p.doctor_id
   GROUP BY d.doctor_id, d.name;
   ```

3. **Names of Patients Who Have Not Been Assigned a Doctor:**
   ```sql
   SELECT name 
   FROM Patients
   WHERE doctor_id IS NULL;
   ```

4. **Specializations of Doctors with More Than 10 Patients Assigned:**
   ```sql
   SELECT d.specialization
   FROM Doctors d
   JOIN Patients p ON d.doctor_id = p.doctor_id
   GROUP BY d.doctor_id, d.specialization
   HAVING COUNT(p.patient_id) > 10;
   ```

5. **Patient Names and Corresponding Diseases for Patients Assigned to a Specific Doctor:**
   ```sql
   SELECT p.name AS patient_name, p.disease
   FROM Patients p
   WHERE p.doctor_id = <doctor_id>;
   ```
   Replace `<doctor_id>` with the specific doctor's ID you want to query.
