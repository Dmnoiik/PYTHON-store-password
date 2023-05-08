from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]

    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]

    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, string=password)
    pyperclip.copy(password_entry.get())


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_credentials():
    website = website_entry.get()
    login = login_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": login,
        "password": password
    }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title='Error', message='One of the fields is empty, either password or website')
    else:
        try:
            with open('data.json', mode='r') as file:
                try:
                    # data is a dictionary
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    # Empty dicitonary if nothing in the file
                    data = {}
        except FileNotFoundError:
            data = new_data
        else:
            ## Update DICTIONARY -> adds new key if missing or updates
            if website in data:
                is_ok = messagebox.askokcancel(message='Password is already stored\nDo you want to overwrite it?')
                if is_ok:
                    data.update(new_data)

            data.update(new_data)


        finally:
            with open('data.json', mode='w') as file:
                json.dump(data, file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website = website_entry.get()
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning('Warning', message='No passwords are stored yet. Please store new password')

    else:
        try:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(website, message=f"Email: {email}\nPassword: {password}")
        except KeyError:
            messagebox.showwarning(title='Empty',
                                   message='Such website is not stored anywhere (or is empty)')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=20, pady=20)
window.title("Password generator")
# Image
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
logo = canvas.create_image(100, 100, image=logo_img)

# Text
website_label = Label(text='Website:', font=("Ariel", 10, 'normal'))
login_label = Label(text='Email/Username:', font=("Ariel", 10, 'normal'))
password_label = Label(text='Password:', font=("Ariel", 10, 'normal'))

# Entries
website_entry = Entry(width=42)
website_entry.focus()
login_entry = Entry(width=52)
login_entry.insert(index=0, string='d.marszalkiewicz2000@gmail.com')
password_entry = Entry(width=30)

# Buttons
generate_button = Button(text='Generate Password', command=generate_password)
add_button = Button(text='Add', width=35, command=save_credentials)
search_button = Button(text="Search", command=search)

# Grid
canvas.grid(column=1, row=0)
website_label.grid(column=0, row=1)
login_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

website_entry.grid(column=1, row=1, columnspan=2, sticky='EW')
login_entry.grid(column=1, row=2, columnspan=2, sticky='EW')
password_entry.grid(column=1, row=3, sticky='EW')

generate_button.grid(column=2, row=3, sticky='EW')
add_button.grid(column=1, row=4, columnspan=2, sticky='EW')
search_button.grid(column=2, row=1, sticky='EW')
window.mainloop()
