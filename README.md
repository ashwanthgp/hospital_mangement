# hospital_mangement
Hospital Management Application using python and sql

  It is a simple hospital management application created using python and mysql connector. It consistes of an login window .After successful login it displays the main window ,which is hidden until then.
The application has 5 options,
1)register patient
2)view patient records
3)delete patient records
4)book appointment
5)view appointment



Steps

1)Install mysql-connector

pip install mysql-connector-python

2)SQL COMMANDS,

Create a database hospital_management and use the database then execute the following commands to create tables

CREATE TABLE patients (patient_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), dob DATE, contact VARCHAR(255), medical_history TEXT);

CREATE TABLE doctors (doctor_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), specialization VARCHAR(255));

CREATE TABLE appointments (appointment_id INT AUTO_INCREMENT PRIMARY KEY, patient_id INT, doctor_id INT, appointment_date DATE, FOREIGN KEY (patient_id) REFERENCES patients(patient_id), FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id));

![hos1](https://github.com/ashwanthgp/hospital_mangement/assets/144984536/9d4fab82-78d7-4c40-97af-a3ba871edd03)


![hos2](https://github.com/ashwanthgp/hospital_mangement/assets/144984536/4f3810b2-bcf0-408f-874a-3b0e500a1fe5)

