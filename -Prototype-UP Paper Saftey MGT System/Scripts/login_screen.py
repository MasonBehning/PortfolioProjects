import tkinter as tk
import subprocess

# Global variables
username_entry = None
password_entry = None
status_label = None


def login():
    global username_entry, password_entry, status_label

    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "admin":
        status_label.config(text="Login successful", fg="green")
        subprocess.Popen(["python", "main.py"])
    else:
        status_label.config(text="Invalid username or password", fg="red")


def create_login_window():
    global username_entry, password_entry, status_label

    login_window = tk.Toplevel(root)
    login_window.geometry("550x450")  # Adjusted dimensions to accommodate the image
    login_window.title("Login")

    logo_image = tk.PhotoImage(file="cropped-UPPapersLogo-1-removebg-preview.png")
    logo_label = tk.Label(login_window, image=logo_image)
    logo_label.image = logo_image  # Keep a reference to prevent garbage collection
    logo_label.pack(pady=(10, 20))  # Adjusted padding to make the image look better

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack()

    status_label = tk.Label(login_window, text="")
    status_label.pack()

    return login_window


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")

    login_window = create_login_window()

    root.mainloop()
