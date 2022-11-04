import tkinter
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, tkinter.END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letter_generator = [random.choice(letters) for char in range(nr_letters)]
    symbols_generator = [random.choice(symbols) for char in range(nr_symbols)]
    numbers_generator = [random.choice(numbers) for char in range(nr_numbers)]

    password_list = letter_generator + symbols_generator + numbers_generator
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    password = password_input.get()
    email = email_input.get()
    website = (website_input.get()).capitalize()
    new_data = {
        website: {
            "email": email,
            "password": password,

        }
    }
    if len(password) == 0 or len(website) == 0 or len(email) == 0:
        messagebox.showinfo(message="Please don't leave any fields empty")

    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)


        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            password_input.delete(0, tkinter.END)
            website_input.delete(0, tkinter.END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = (website_input.get()).capitalize()
    print(website)
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            searched_email = data[f"{website}"]["email"]
            searched_password = data[f"{website}"]["password"]
    except FileNotFoundError:
        messagebox.showinfo(title= "oops", message = "No Data File Found")
    except KeyError:
        messagebox.showinfo(title= "oops", message = "No details for this website exists")

    else:

        for dicts in data:
            if dicts == website:
                messagebox.showinfo(title="Info", message=f"Website : {website}"
                                                          f"\n Email : {searched_email}"
                                                          f"\n Password : {searched_password}")


# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=30, pady=20)

canvas = tkinter.Canvas(width=200, height=200)
lock = tkinter.PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=lock)
canvas.grid(row=1, column=2)

# Website
website_text = tkinter.Label(text="Website:")
website_text.grid(row=2, column=1)

website_input = tkinter.Entry(width=21)
website_input.grid(row=2, column=2)
website_input.focus()

# Email/Username
email_text = tkinter.Label(text="Email/Username:")
email_text.grid(row=3, column=1)

email_input = tkinter.Entry(width=35)
email_input.grid(row=3, column=2, columnspan=2)
email_input.insert(0, "aurick@gmail.com")

# Password
password_text = tkinter.Label(text="Password:")
password_text.grid(row=4, column=1)

password_input = tkinter.Entry(width=21)
password_input.grid(row=4, column=2)

# Generate Password
gen_pass = tkinter.Button(text="Generate Password", width=10, command=generate_password)
gen_pass.grid(row=4, column=3)

# Add
add_button = tkinter.Button(text="Add", width=33, command=save)
add_button.grid(row=5, column=2, columnspan=2)

# Search
search_button = tkinter.Button(text="Search", width=10, command=search_password)
search_button.grid(row=2, column=3)

window.mainloop()
