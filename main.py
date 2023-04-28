from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8,10))]

    symbols_list = [choice(symbols) for _ in range(randint(2,4))]

    numbers_list = [choice(numbers) for _ in range(randint(2,4))]
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

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title='Error', message='One of the fields is empty, either password or website')
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \nEmail: {login}\nPassword: {password}"
                                               f" \nIs it okay to save?")
        if is_ok:
            with open('data.txt', mode='a') as file:
                file.write(f"Page: {website} | login: {login} | Password: {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)


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
website_entry = Entry(width=52)
website_entry.focus()
login_entry = Entry(width=52)
login_entry.insert(index=0, string='d.marszalkiewicz2000@gmail.com')
password_entry = Entry(width=30)

# Buttons
generate_button = Button(text='Generate Password', command=generate_password)
add_button = Button(text='Add', width=44, command=save_credentials)

# Grid
canvas.grid(column=1, row=0)
website_label.grid(column=0, row=1)
login_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

website_entry.grid(column=1, row=1, columnspan=2, sticky='w')
login_entry.grid(column=1, row=2, columnspan=2, sticky='w')
password_entry.grid(column=1, row=3, sticky='w')

generate_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
