from tkinter import *


def get_user_info():
    username, password, elevance, suppress, continued = show_gui()
    return username, password, elevance, suppress, continued


def show_gui():
    root = Tk()
    root.title("Accessibility Checker")

    # Define a larger font
    large_font = ('Helvetica', 16)

    Label(root, text="Please provide the username and password for an activated test user.\n", font=large_font).grid(
        row=0, columnspan=2, padx=10, pady=10)

    Label(root, text="Username:", font=large_font).grid(row=2, padx=10, pady=10)
    Label(root, text="Password:", font=large_font).grid(row=3, padx=10, pady=10)

    username_entry = Entry(root, font=large_font)
    password_entry = Entry(root, font=large_font)

    username_entry.grid(row=2, column=1, padx=10, pady=10)
    password_entry.grid(row=3, column=1, padx=10, pady=10)

    # Add Continue Session checkbox
    continue_var = BooleanVar()
    continue_checkbox = Checkbutton(root, text="Continue Session?", variable=continue_var, font=large_font)
    continue_checkbox.grid(row=4, columnspan=2, pady=10)

    # Add Elevance checkbox
    elevance_var = BooleanVar()
    elevance_checkbox = Checkbutton(root, text="Is Elevance Client?", variable=elevance_var, font=large_font)
    elevance_checkbox.grid(row=5, columnspan=2, pady=10)

    # Add Suppress checkbox
    suppress_var = BooleanVar(value=True)
    suppress_checkbox = Checkbutton(root, text="Suppress Known Issues (Recommended)?", variable=suppress_var, font=large_font)
    suppress_checkbox.grid(row=6, columnspan=2, pady=10)

    Button(root, text='Submit', command=root.quit, font=large_font).grid(row=7, column=1, sticky=W, pady=10)
    Button(root, text='Cancel', command=root.destroy, font=large_font).grid(row=7, column=0, sticky=E, pady=10)

    root.mainloop()

    username = username_entry.get()
    password = password_entry.get()
    elevance = elevance_var.get()
    suppress = suppress_var.get()
    continued = continue_var.get()

    root.destroy()

    return username, password, elevance, suppress, continued


if __name__ == "__main__":
    username, password, elevance, suppress, continued = get_user_info()
    print(f"Username: {username}, Password: {password}, Elevance: {elevance}, Suppress: {suppress}, Continued: {continued}")
    print("User information retrieved successfully.")