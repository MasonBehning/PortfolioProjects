import os
import tkinter as tk
import tkinter.filedialog as filedialog
import mysql.connector
from mysql.connector import errorcode
from tkinter import ttk
import tkinter.messagebox as messagebox

class ViewAllReportsGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

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

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the table
        table_frame = tk.LabelFrame(self, text="Reports")
        table_frame.pack(fill="both", expand="yes", padx=20, pady=20)

        # Create a Treeview widget to display the data as a table
        self.table = ttk.Treeview(table_frame)
        self.table.pack(side="left", fill="both", expand="yes")

        # Configure columns
        self.table["columns"] = ("ManagerApprovalYN", "Date", "Time", "Description", "WitnessYN", "MedicalYN", "ReportType", "EmployeeID", "RemedyID", "AlertID")
        self.table.column("#0", width=0, stretch=tk.NO)
        for col in self.table["columns"]:
            self.table.column(col, anchor=tk.CENTER, width=100)
            self.table.heading(col, text=col, anchor=tk.CENTER)

        # Create a scrollbar for the table
        scrollbar = tk.Scrollbar(table_frame, orient="vertical")
        scrollbar.config(command=self.table.yview)
        scrollbar.pack(side="right", fill="y")

        self.table.config(yscrollcommand=scrollbar.set)

        # Load the data from the database
        self.load_data()

    def load_data(self):
        # Fetch data from the database
        self.cursor.execute("SELECT * FROM IncidentReport")
        rows = self.cursor.fetchall()

        # Insert each row into the table
        for row in rows:
            self.table.insert("", "end", values=row)

def main():
    root = tk.Tk()
    root.title("View All Reports GUI")
    app = ViewAllReportsGUI(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
