import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from tkinter import Toplevel
from tkinter import Tk, Button, Entry, Label, Toplevel
from tkinter import PhotoImage
from PIL import Image, ImageTk




class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="app123LL",
            database="hospital_management"
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print("Database Error:", str(e))
            self.conn.rollback()

    def fetch_data(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def insert_patient(self, name, dob, contact, medical_history):
        query = "INSERT INTO patients (name, dob, contact, medical_history) VALUES (%s, %s, %s, %s)"
        values = (name, dob, contact, medical_history)
        self.execute_query(query, values)

    def book_appointment(self, patient_id, doctor_id, appointment_date):
        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)"
        #CREATE TABLE appointments ( patient_id INT PRIMARY KEY, doctor_id INT, appointment_date DATE );
        values = (patient_id, doctor_id, appointment_date)
        self.execute_query(query, values)

    def get_patient_records(self):
        query = "SELECT * FROM patients"
        return self.fetch_data(query)
    
    def delete_patient(self, patient_id):
        query = "DELETE FROM patients WHERE patient_id = %s"
        values = (patient_id,)
        self.execute_query(query, values)

    def get_appointment_details(self):
        query = "SELECT * FROM appointments "
        #values = (patient_id,)
        return self.fetch_data(query)

    def close(self):
        self.cursor.close()
        self.conn.close()

class HospitalManagementApp:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Hospital Management System")
        
          # Set the main window size
        self.root.geometry("800x700")
       
        
        root.configure(bg='grey')

        # Load and place the background image on the canvas
        background_image = Image.open("h1.png")  # Replace with your image file
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(root, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo  # Prevent garbage collection

        style = ttk.Style()
        style.theme_use("alt")
        title_label = ttk.Label(self.root, text="APOLLO HOSPITAL", font=("Helvetica", 24, "bold"), foreground="blue", background="lightgray")
        title_label.pack(pady=20)
        
        
        '''self.view_appointments_window = tk.Toplevel(root)
        self.view_appointments_window.title("View Appointments")

        self.patient_id_label = ttk.Label(self.view_appointments_window, text="Patient ID:")
        self.patient_id_entry = ttk.Entry(self.view_appointments_window)
        self.patient_id_label.pack()
        self.patient_id_entry.pack()'''

        self.db = db  # Initialize the database connection
       
        # Create a login frame
        self.login_frame = ttk.Frame(self.root,width=50,height=100)
        self.login_frame.pack(fill=tk.BOTH, expand=True, padx=250, pady=250)


        # Create login widgets with ttk style
        self.username_label = ttk.Label(self.login_frame, text="Username:")
        self.username_entry = ttk.Entry(self.login_frame)
        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_entry = ttk.Entry(self.login_frame, show="*")

        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Create the main GUI frame but initially hide it
        #self.gui_frame = ttk.Frame(self.root)
        self.gui_frame = ttk.Frame(self.root, width=300, height=200)

        # Initialize buttons without displaying them
        
        self.register_button = ttk.Button(self.gui_frame, text="Register Patient", command=self.register_patient)
        self.book_appointment_button = ttk.Button(self.gui_frame, text="Book Appointment", command=self.book_appointment)
        self.view_records_button = ttk.Button(self.gui_frame, text="View Patient Records", command=self.view_patient_records)
        self.delete_records_button = ttk.Button(self.gui_frame, text="Delete Patient Records", command=self.delete_patient_records)
        self.view_appointments_button = ttk.Button(self.gui_frame, text="View Appointments", command=self.view_appointments)

        # Place buttons at the center of the frame with padding
        self.register_button.grid(row=0, column=0, padx=10, pady=10)
        self.book_appointment_button.grid(row=0, column=1, padx=10, pady=10)
        self.view_records_button.grid(row=0, column=2, padx=10, pady=10)
        self.delete_records_button.grid(row=1, column=0, padx=10, pady=10)
        self.view_appointments_button.grid(row=1, column=1, padx=10, pady=10)


    def login(self):
        # Get username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Perform authentication (you should implement this logic)
        if self.authenticate(username, password):
            # Successful login
            self.login_frame.pack_forget()  # Hide the login frame
            # Load the background image
            self.root.geometry("1200x900")
            
            #   a   self.gui_frame = ttk.Frame(self.root, bg='grey')
            # self.gui_frame.configure(bg='grey') 
            self.gui_frame.pack(fill=tk.BOTH, expand=True, padx=250, pady=250)  # Show the main GUI frame
            

            # Show the buttons for registered users
            self.register_button.grid(row=1, column=0, padx=10, pady=10)
            self.book_appointment_button.grid(row=1, column=1, padx=10, pady=10)
            self.view_records_button.grid(row=1, column=2, padx=10, pady=10)
            self.delete_records_button.grid(row=1, column=3, padx=10, pady=10)
            self.view_appointments_button.grid(row=1, column=4, padx=10, pady=10)

            # Load and place images above the buttons
            records_image = tk.PhotoImage(file="records.png")
            patient_image = tk.PhotoImage(file="patient.png")
            appointment_image = tk.PhotoImage(file="appointment.png")
            delete_records_image = tk.PhotoImage(file="delete_patients.png")
            view_appointments_image = tk.PhotoImage(file="view_appointments.png")

            records_label = ttk.Label(self.gui_frame, image=records_image, compound="bottom")
            patient_label = ttk.Label(self.gui_frame, image=patient_image, compound="bottom")
            appointment_label = ttk.Label(self.gui_frame, image=appointment_image,compound="bottom")
            delete_records_label = ttk.Label(self.gui_frame, image=delete_records_image, compound="bottom")
            view_appointments_label = ttk.Label(self.gui_frame, image=view_appointments_image, compound="bottom")

            # Keep references to PhotoImage objects to prevent garbage collection
            records_label.image = records_image
            patient_label.image = patient_image
            appointment_label.image = appointment_image
            delete_records_label.image = delete_records_image
            view_appointments_label.image = view_appointments_image

            records_label.grid(row=0, column=0)
            patient_label.grid(row=0, column=1)
            appointment_label.grid(row=0, column=2)
            delete_records_label.grid(row=0, column=3, padx=10)
            view_appointments_label.grid(row=0, column=4, padx=10)

            
            
        else:
            # Unsuccessful login (you should handle this case)
            messagebox.showerror("Login Failed", "Invalid username or password")

    def authenticate(self, username, password):
        # Implement your authentication logic here
        # You can use a database table to check credentials
        # For the example, we'll use hardcoded values
        if username == "admin" and password == "admin123":
            return True
        else:
            return False

    def register_patient(self):
        # Create a new window for patient registration
        registration_window = Toplevel(self.root)
        registration_window.title("Register Patient")

        background_image = Image.open("h1.png")  # Replace with your image file
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(registration_window, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo 

        # Create and place Entry widgets for patient information
        name_label = Label(registration_window, text="Name:")
        name_entry = Entry(registration_window)
        name_label.pack()
        name_entry.pack()

        dob_label = Label(registration_window, text="Date of Birth:")
        dob_entry = Entry(registration_window)
        dob_label.pack()
        dob_entry.pack()

        contact_label = Label(registration_window, text="Contact:")
        contact_entry = Entry(registration_window)
        contact_label.pack()
        contact_entry.pack()

        medical_history_label = Label(registration_window, text="Medical History:")
        medical_history_entry = Entry(registration_window)
        medical_history_label.pack()
        medical_history_entry.pack()

        def submit_registration():
            # Get data from Entry widgets
            name = name_entry.get()
            dob = dob_entry.get()
            contact = contact_entry.get()
            medical_history = medical_history_entry.get()

            # Insert patient data into the database
            self.db.insert_patient(name, dob, contact, medical_history)

            # Close the registration window
            registration_window.destroy()

        submit_button = Button(registration_window, text="Submit", command=submit_registration)
        submit_button.pack()
        pass

    def book_appointment(self):
        # Create a new window for appointment booking
        appointment_window = Toplevel(self.root)
        appointment_window.title("Book Appointment")

        background_image = Image.open("h1.png")  # Replace with your image file
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(appointment_window, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo 

        # Create and place Entry widgets for appointment details
        patient_id_label = Label(appointment_window, text="Patient ID:")
        patient_id_entry = Entry(appointment_window)
        patient_id_label.pack()
        patient_id_entry.pack()

        doctor_id_label = Label(appointment_window, text="Doctor ID:")
        doctor_id_entry = Entry(appointment_window)
        doctor_id_label.pack()
        doctor_id_entry.pack()

        appointment_date_label = Label(appointment_window, text="Appointment Date:")
        appointment_date_entry = Entry(appointment_window)
        appointment_date_label.pack()
        appointment_date_entry.pack()

        def submit_appointment():
            # Get data from Entry widgets
            patient_id = patient_id_entry.get()
            doctor_id = doctor_id_entry.get()
            appointment_date = appointment_date_entry.get()

            # Book the appointment in the database
            self.db.book_appointment(patient_id, doctor_id, appointment_date)

            # Close the appointment booking window
            appointment_window.destroy()

        submit_button = Button(appointment_window, text="Submit", command=submit_appointment)
        submit_button.pack()
        pass

    def view_patient_records(self):
        view_records_window = tk.Toplevel(self.root)
        view_records_window.title("View Patient Records")

        background_image = Image.open("h1.png")  # Replace with your image file
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(view_records_window, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo

        # Create a Treeview widget to display records
        tree = ttk.Treeview(view_records_window, columns=("Patient ID","Name", "Date of Birth", "Contact", "Medical History"))
        tree.heading("#1", text="Patient ID",anchor="w")
        tree.heading("#2", text="Name", anchor="w")
        tree.heading("#3", text="Date of Birth", anchor="w")
        tree.heading("#4", text="Contact", anchor="w")
        tree.heading("#5", text="Medical History", anchor="w")

        # Set column widths explicitly
        tree.column("#0", width=0,stretch=tk.NO)  # Hide the default first column
        tree.column("#1", width=150)
        tree.column("#2", width=150)
        tree.column("#3", width=150)
        tree.column("#4", width=200) 
        tree.column("#5", width=200) # Adjust the width as needed

        # Set column anchor to 'w' (west) to align text to the left
        for col in ("#1", "#2", "#3", "#4","#5"):
            tree.heading(col, anchor="w")

        # Fetch patient records from the database
        records = self.db.get_patient_records()

        # Insert patient records into the Treeview
        for record in records:
            # Insert values into the Treeview, setting the 'values' parameter explicitly
            tree.insert("", "end", values=(record[0],record[1], record[2], record[3],record[4]))

        tree.pack()



    def delete_patient_records(self):
        # Create a new window for deleting patient records
        delete_records_window = Toplevel(self.root)
        delete_records_window.title("Delete Patient Records")

        background_image = Image.open("h1.png")  # Replace with your image file
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(delete_records_window, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo 


        # Create and place Entry widgets for patient ID
        patient_id_label = Label(delete_records_window, text="Patient ID:")
        patient_id_entry = Entry(delete_records_window)
        patient_id_label.pack()
        patient_id_entry.pack()

        def delete_record():
            # Get the patient ID to delete
            patient_id = patient_id_entry.get()

            # Delete the patient record from the database
            self.db.delete_patient(patient_id)

            # Close the delete records window
            delete_records_window.destroy()

        delete_button = Button(delete_records_window, text="Delete", command=delete_record)
        delete_button.pack()

    def view_appointments(self):
        # Create a new window for viewing appointments
        view_appointments_window = tk.Toplevel(self.root)
        view_appointments_window.title("View Appointments")

        background_image = Image.open("h1.png")  # Replace with your image file
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(view_appointments_window, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo

        # Create a Treeview widget to display appointments
        tree = ttk.Treeview(view_appointments_window, columns=("Patient ID", "Doctor ID", "Appointment Date"))
        tree.heading("#1", text="Patient ID", anchor="w")
        tree.heading("#2", text="Doctor ID", anchor="w")
        tree.heading("#3", text="Appointment Date", anchor="w")

        tree.column("#0", width=0,stretch=tk.NO)  # Hide the default first column
        tree.column("#1", width=150)
        tree.column("#2", width=150)
        tree.column("#3", width=150)


        # Set column anchor to 'w' (west) to align text to the left
        for col in ("#1", "#2", "#3"):
            tree.heading(col, anchor="w")

        # Fetch appointment details from the database
        appointments = self.db.get_appointment_details()

        # Insert appointment records into the Treeview
        for appointment in appointments:
            # Insert values into the Treeview, setting the 'values' parameter explicitly
            tree.insert("", "end", values=(appointment[0], appointment[1], appointment[2]))

        tree.pack()




if __name__ == "__main__":
    root = tk.Tk()
    db = Database()  # Create a Database instance
    app = HospitalManagementApp(root, db)
    
    
    root.mainloop()
