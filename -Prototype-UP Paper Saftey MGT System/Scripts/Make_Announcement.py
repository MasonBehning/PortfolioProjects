import tkinter as tk
import tkinter.filedialog as filedialog
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

config = {
    'user': 'sp2023bis425oc1g3',
    'password': 'warm',
    'host': 'sp2023bis425oc1g3.mysql.db',
    'database': 'sp2023bis425oc1g3',
    'raise_on_warnings': True,
}

def get_email_list():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT email FROM Employee"
    cursor.execute(query)
    email_list = [email[0] for email in cursor.fetchall()]
    cursor.close()
    connection.close()
    return email_list

def get_latest_incident():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT title, description FROM Incident ORDER BY date DESC LIMIT 1"
    cursor.execute(query)
    latest_incident = cursor.fetchone()
    cursor.close()
    connection.close()
    return latest_incident

def send_email(to_list, subject, body, attachments):
    """
    Sends an email to the specified email list with the given subject, body, and attachments.
    """
    # Set up email message
    message = MIMEMultipart()
    message['To'] = ', '.join(to_list)
    message['Subject'] = subject
    message.attach(MIMEText(body))

    # Attach files
    for attachment in attachments:
        with open(attachment, 'rb') as file:
            part = MIMEApplication(file.read(), Name=attachment)
            part['Content-Disposition'] = f'attachment; filename="{attachment}"'
            message.attach(part)

    # Set up SMTP server and send email
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login('your_email@gmail.com', 'your_email_password')
    smtp_server.sendmail('your_email@gmail.com', to_list, message.as_string())
    smtp_server.quit()

def browse_files():
    """
    Opens a file browser dialog and returns the selected file paths.
    """
    file_paths = filedialog.askopenfilenames()
    file_listbox.delete(0, tk.END)
    for file_path in file_paths:
        file_listbox.insert(tk.END, file_path)

def on_submit():
    # Get input values
    title = title_entry.get()
    description = desc_entry.get('1.0', tk.END)

    # Get email list and latest incident
    to_list = get_email_list()
    latest_incident_title, latest_incident_desc = get_latest_incident()

    # Send email
    subject = f"{title} Announcement"
    body = f"{title}\n\n{description}\n\nLatest Incident:\n{latest_incident_title}\n{latest_incident_desc}"
    attachments = file_listbox.get(0, tk.END)
    send_email(to_list, subject, body, attachments)

    # Clear input fields
    title_entry.delete(0, tk.END)
    desc_entry.delete('1.0', tk.END)
    file_listbox.delete(0, tk.END)

def create_message_board():
    message_board = tk.Toplevel()
    message_board.geometry("750x600")
    message_board.title("Make Announcement")

    title_label = tk.Label(message_board, text="Title:", font=("Arial", 16, 'bold'))
    title_label.pack(pady=(20, 10), padx=20)

    title_entry = tk.Entry(message_board, font=("Arial", 16))
    title_entry.pack(pady=(0, 20), padx=20, fill=tk.X)

    desc_label = tk.Label(message_board, text="Description:", font=("Arial", 16, 'bold'))
    desc_label.pack(pady=(0, 10), padx=20)

    desc_entry = tk.Text(message_board, font=("Arial", 14), height=10)
    desc_entry.pack(pady=(0, 20), padx=20, fill=tk.BOTH, expand=True)

    file_label = tk.Label(message_board, text="Attachments:", font=("Arial", 16, 'bold'))
    file_label.pack(pady=(0, 10), padx=20)

    file_listbox = tk.Listbox(message_board, font=("Arial", 14), height=5)
    file_listbox.pack(pady=(0, 20), padx=20, fill=tk.BOTH, expand=True)

    browse_btn = tk.Button(message_board, text="Add Attachments", font=("Arial", 14), command=browse_files)
    browse_btn.pack(pady=(0, 10), padx=20, fill=tk.X)

    send_btn = tk.Button(message_board, text="Send", font=("Arial", 16), command=on_submit)
    send_btn.pack(pady=(0, 20), padx=20, fill=tk.X)

    message_board.mainloop()

if __name__ == "__main__":
    create_message_board()
