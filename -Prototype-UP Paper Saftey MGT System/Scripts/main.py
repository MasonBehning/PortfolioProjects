import tkinter as tk
import mysql.connector
import os

user = "sp2023bis425oc1g3"
password = "warm"
host = "141.209.241.88"
database = "sp2023bis425oc1g3"
connection_name = "BIS 425"

def get_latest_incident():
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()
    query = "SELECT Date, Description, RemedyID FROM IncidentReport ORDER BY Date DESC, Time DESC LIMIT 1;"
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    cnx.close()
    return (row[0], row[1], get_remedy_description(row[2]))

def get_remedy_description(remedy_id):
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    cursor = cnx.cursor()
    query = "SELECT Description FROM Remedy WHERE RemedyID = %s;"
    cursor.execute(query, (remedy_id,))
    row = cursor.fetchone()
    cursor.close()
    cnx.close()
    return row[0] if row else ""

def on_make_announcement():
    os.system("python Make_Announcement.py")

def on_view_all_reports():
    os.system("python View_All_Reports.py")

def on_report_incident():
    os.system("python Report_Incident.py")

main_window = tk.Tk()
main_window.geometry("1000x600")
main_window.title("UP Paper Safety Management")

left_frame = tk.Frame(main_window, bd=2, relief=tk.RIDGE)
left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

logo_image = tk.PhotoImage(file="./cropped-UPPapersLogo-1-removebg-preview.png")
logo_label = tk.Label(left_frame, image=logo_image)
logo_label.image = logo_image
logo_label.pack(pady=(20, 40))

incident_label = tk.Label(left_frame, text="Latest Incident:", font=("Arial", 24, 'bold'), justify=tk.LEFT)
incident_label.pack(pady=(0, 10), padx=20)

latest_incident = get_latest_incident()

date_label = tk.Label(left_frame, text=f"Date: {latest_incident[0]}", font=("Arial", 16, 'bold'), justify=tk.LEFT)
date_label.pack(pady=(0, 5), padx=20)

desc_label = tk.Label(left_frame, text=f"Description: {latest_incident[1]}", font=("Arial", 16), justify=tk.LEFT)
desc_label.pack(pady=(0, 5), padx=20)

remedy_label = tk.Label(left_frame, text=f"Remedy: {latest_incident[2]}", font=("Arial", 16), justify=tk.LEFT)
remedy_label.pack(pady=(0, 5), padx=20)

right_frame = tk.Frame(main_window, bd=2, relief=tk.RIDGE)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

make_announcement_btn = tk.Button(right_frame, text="Make Announcement", font=("Arial", 18), command=on_make_announcement)
make_announcement_btn.pack(fill=tk.X, ipady=20, pady=(0, 10))

view_all_reports_btn = tk.Button(right_frame, text="View All Reports", font=("Arial", 18), command=on_view_all_reports)
view_all_reports_btn.pack(fill=tk.X, ipady=20, pady=(0, 10))

report_incident_btn = tk.Button(right_frame, text="Report Incident", font=("Arial", 18), command=on_report_incident)
report_incident_btn.pack(fill=tk.X, ipady=20, pady=(0, 10))

main_window.mainloop()

