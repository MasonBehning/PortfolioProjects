import tkinter as tk
import os
import tkinter.messagebox as messagebox
import mysql.connector
from mysql.connector import errorcode

class IncidentReportGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        # Connect to the database
        try:
            self.cnx = mysql.connector.connect(user='sp2023bis425oc1g3', password='warm',
                                                host='141.209.241.88', database='sp2023bis425oc1g3')
            self.cursor = self.cnx.cursor()
            messagebox.showinfo("Success", "Database connection established successfully!")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                messagebox.showerror("Error", "Access denied: Invalid credentials.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                messagebox.showerror("Error", "Database not found.")
            else:
                messagebox.showerror("Error", err)

    def create_widgets(self):
        # Report Details
        details_frame = tk.LabelFrame(self, text="Report Details")
        details_frame.pack(fill="both", expand="yes", padx=20, pady=20)

        # Manager Approval
        self.manager_approval_lbl = tk.Label(details_frame, text="Manager Approval Y/N:")
        self.manager_approval_lbl.pack()
        self.manager_approval_entry = tk.Entry(details_frame)
        self.manager_approval_entry.pack()

        # Date
        self.date_lbl = tk.Label(details_frame, text="Date:")
        self.date_lbl.pack()
        self.date_entry = tk.Entry(details_frame)
        self.date_entry.pack()

        # Time
        self.time_lbl = tk.Label(details_frame, text="Time:")
        self.time_lbl.pack()
        self.time_entry = tk.Entry(details_frame)
        self.time_entry.pack()

        # Description
        self.description_lbl = tk.Label(details_frame, text="Description:")
        self.description_lbl.pack()
        self.description_entry = tk.Entry(details_frame)
        self.description_entry.pack()

        # Witness
        self.witness_lbl = tk.Label(details_frame, text="Witness Y/N:")
        self.witness_lbl.pack()
        self.witness_entry = tk.Entry(details_frame)
        self.witness_entry.pack()

        # Medical
        self.medical_lbl = tk.Label(details_frame, text="Medical Y/N:")
        self.medical_lbl.pack()
        self.medical_entry = tk.Entry(details_frame)
        self.medical_entry.pack()

        # Report Type
        self.report_type_lbl = tk.Label(details_frame, text="Report Type:")
        self.report_type_lbl.pack()
        self.report_type_entry = tk.Entry(details_frame)
        self.report_type_entry.pack()

        # Employee ID
        self.employee_id_lbl = tk.Label(details_frame, text="Employee ID:")
        self.employee_id_lbl.pack()
        self.employee_id_entry = tk.Entry(details_frame)
        self.employee_id_entry.pack()

        # Remedy ID
        self.remedy_id_lbl = tk.Label(details_frame, text="Remedy ID:")
        self.remedy_id_lbl.pack()
        self.remedy_id_entry = tk.Entry(details_frame)
        self.remedy_id_entry.pack()

        # Alert ID
        self.alert_id_lbl = tk.Label(details_frame, text="Alert ID:")
        self.alert_id_lbl.pack()
        self.alert_id_entry = tk.Entry(details_frame)
        self.alert_id_entry.pack()

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack()

    def submit(self):
        # Retrieve values from entries
        manager_approval = self.manager_approval_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        description = self.description_entry.get()
        witness = self.witness_entry.get()
        medical = self.medical_entry.get()
        report_type = self.report_type_entry.get()
        employee_id = self.employee_id_entry.get()
        remedy_id = self.remedy_id_entry.get()
        alert_id = self.alert_id_entry.get()

        # Insert the data into the database
        try:
            add_report = ("""INSERT INTO IncidentReport 
                            (ManagerApprovalYN, Date, Time, Description, WitnessYN, MedicalYN, ReportType, EmployeeID, RemedyID, AlertID) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            report_data = (manager_approval, date, time, description, witness, medical, report_type, employee_id, remedy_id, alert_id)
            self.cursor.execute(add_report, report_data)
            self.cnx.commit()

            messagebox.showinfo("Success", "Report saved successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", err)

    def generate_report(self, manager_approval, date, time, description, witness, medical, report_type, employee_id, remedy_id, alert_id):
        report = f"""Manager Approval: {manager_approval}
Date: {date}
Time: {time}
Description: {description}
Witness: {witness}
Medical: {medical}
Report Type: {report_type}
Employee ID: {employee_id}
Remedy ID: {remedy_id}
Alert ID: {alert_id}
"""
        return report

def main():
    root = tk.Tk()
    root.title("Incident Report GUI")
    app = IncidentReportGUI(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
