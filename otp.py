# Importing the libraries
from twilio.rest import Client
import random
import tkinter as tk
from tkinter import messagebox

# Creating Window
root = tk.Tk()
root.title("OTP Verification")
root.geometry("600x550")

# Twilio account details
account_sid = "Your_twilio_SID"
auth_token = "Your_twilio_auth_token"

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Global variable for OTP and mobile number
n = random.randint(100000, 999999)
initial_mobile_number = ""

# Function to send OTP
def send_otp():
    global n, initial_mobile_number
    country_code = country_code_entry.get()
    mobile_number = mobile_number_entry.get()
    full_number = f"{country_code}{mobile_number}"
    initial_mobile_number = full_number
    n = random.randint(1000, 9999)
    client.messages.create(
        to=full_number, 
        from_="Your_twilio_phone_number", 
        body=f"Your OTP is {n}"
    )
    messagebox.showinfo("showinfo", f"OTP sent to {full_number}")
    send_otp_button.config(state=tk.DISABLED)

# Function to resend OTP
def resend_otp():
    global n
    n = random.randint(1000, 9999)
    country_code = country_code_entry.get()
    mobile_number = mobile_number_entry.get()
    full_number = f"{country_code}{mobile_number}"
    client.messages.create(
        to=full_number, 
        from_="Your_twilio_phone_number", 
        body=f"Your OTP is {n}"
    )
    messagebox.showinfo("showinfo", f"OTP resent to {full_number}")

# Function to check the OTP
def check_otp():
    global n
    try:
        user_input = int(otp_entry.get())
        if user_input == n:
            messagebox.showinfo("showinfo", "Login Success")
            n = "done"
        elif n == "done":
            messagebox.showinfo("showinfo", "Already entered")
        else:
            messagebox.showinfo("showinfo", "Wrong OTP")
    except ValueError:
        messagebox.showinfo("showinfo", "Invalid OTP")

# Function to enable the Send OTP button when the mobile number is re-entered
def enable_send_otp(event):
    send_otp_button.config(state=tk.NORMAL)
    check_same_mobile_number()

# Function to check if the second entered mobile number is the same as the first
def check_same_mobile_number():
    country_code = country_code_entry.get()
    mobile_number = mobile_number_entry.get()
    full_number = f"{country_code}{mobile_number}"
    if full_number == initial_mobile_number:
        prompt_regenerate_otp()

# Function to prompt if the user wants to regenerate the OTP for the same number
def prompt_regenerate_otp():
    response = messagebox.askquestion("Regenerate OTP", "Do you want to regenerate the OTP for the same number?")
    if response == 'yes':
        resend_otp()
    else:
        messagebox.showinfo("showinfo", "OTP not regenerated")

# Adding '+' prefix to the country code entry
def add_plus_prefix(event):
    if country_code_entry.get() == "":
        country_code_entry.insert(0, '+')

# Drawing the canvas
c = tk.Canvas(root, bg="white", width=400, height=300)
c.place(x=100, y=60)

# Label widget for the application title
login = tk.Label(root, text="OTP Verification", font=("bold", 20), bg="white")
login.place(x=210, y=30)

# Label and entry widget for country code
country_code_label = tk.Label(root, text="Country Code", font=("bold", 15), bg="white")
country_code_label.place(x=100, y=90)
country_code_entry = tk.Entry(root, borderwidth=2, width=5)
country_code_entry.place(x=250, y=95)
country_code_entry.insert(0, '+')
country_code_entry.bind("<FocusIn>", add_plus_prefix)

# Label and entry widget for mobile number
mobile_number_label = tk.Label(root, text="Mobile Number", font=("bold", 15), bg="white")
mobile_number_label.place(x=100, y=130)
mobile_number_entry = tk.Entry(root, borderwidth=2, width=20)
mobile_number_entry.place(x=250, y=135)
mobile_number_entry.bind("<KeyRelease>", enable_send_otp)

# Label and entry widget for OTP
otp_label = tk.Label(root, text="Enter OTP", font=("bold", 15), bg="white")
otp_label.place(x=100, y=170)
otp_entry = tk.Entry(root, borderwidth=2, width=10)
otp_entry.place(x=250, y=175)

# Button to send the initial OTP
send_otp_button = tk.Button(root, text="Send OTP", command=send_otp, font=("bold", 15))
send_otp_button.place(x=100, y=220)

# Submit button
submit_button = tk.Button(root, text="Submit", command=check_otp, font=('bold', 15))
submit_button.place(x=258, y=220)

# Resend Button
resend_button = tk.Button(root, text="Resend OTP", command=resend_otp, font=("bold", 15))
resend_button.place(x=240, y=270)

# Event Loop
root.mainloop()
