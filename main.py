import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os


# Function to create a file or folder
def create_file_or_folder(action, path, name):
    if not name:
        messagebox.showerror("Error", "Name cannot be empty!")
        return

    target_path = os.path.join(path, name)

    if action == 'FILE':
        with open(target_path, 'w'):
            pass
        messagebox.showinfo("Success", f"File '{target_path}' created!")
    elif action == 'FOLDER':
        os.makedirs(target_path, exist_ok=True)
        messagebox.showinfo("Success", f"Folder '{target_path}' created!")

    open_option = messagebox.askyesno("Open", "Open the file/folder?")
    if open_option:
        os.startfile(target_path)

    continue_option = messagebox.askyesno("Continue",
                                          "Continue using DirDynamo?")
    if not continue_option:
        root.destroy()


# Function to delete a file or folder
def delete_file_or_folder(action, path, name):
    if not name:
        messagebox.showerror("Error", "Name cannot be empty!")
        return

    target_path = os.path.join(path, name)

    if os.path.exists(target_path):
        confirm_delete = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{target_path}'?")
        if confirm_delete:
            if action == 'FILE':
                os.remove(target_path)
                messagebox.showinfo("Success",
                                    f"File '{target_path}' deleted!")
            elif action == 'FOLDER':
                os.rmdir(target_path)
                messagebox.showinfo("Success",
                                    f"Folder '{target_path}' deleted!")
        else:
            messagebox.showinfo("Cancelled",
                                f"Deletion of '{target_path}' cancelled.")
    else:
        messagebox.showerror(
            "Error", f"{action.capitalize()} '{target_path}' does not exist!")


# Function to edit a file's content
def edit_file_content(path, edit_type, text):
    global entry_name
    uppath = os.path.join(path, entry_name.get())

    # Check if the path is a directory
    if os.path.isdir(uppath):
        messagebox.showerror(
            "Error",
            f"'{uppath}' is a directory. Please select a file.")
        return

    if not os.path.isfile(uppath):
        messagebox.showerror("Error",
                             f"File '{uppath}' does not exist!")
        return

    if edit_type == 'Append':
        mode = 'a'  # Append mode
    elif edit_type == 'Replace':
        mode = 'w'  # Write mode (replaces existing content)
    else:
        messagebox.showerror("Error", "Invalid edit type!")
        return

    with open(uppath, mode) as f:
        f.write(text)

    messagebox.showinfo("Success", f"File '{uppath}' updated!")

    open_option = messagebox.askyesno("Open", "Open the file?")
    if open_option:
        os.startfile(uppath)

    continue_option = messagebox.askyesno("Continue",
                                          "Continue using DirDynamo?")
    if not continue_option:
        root.destroy()


# Function to browse for a directory
def browse_directory_move():
    global move_var
    directory = filedialog.askdirectory()
    if directory:
        move_var.set(directory)


# Function to browse for a directory
def browse_directory():
    global entry_path
    directory = filedialog.askdirectory()
    if directory:
        entry_path.delete(0, tk.END)
        entry_path.insert(tk.END, directory)


# Function to move a file or folder to a different directory
def move_file_or_folder(path, new_directory):
    global entry_name
    target_path = os.path.join(path, entry_name.get())

    if os.path.exists(target_path):
        new_path = os.path.join(new_directory, entry_name.get())
        os.rename(target_path, new_path)
        messagebox.showinfo("Success",
                            f"'{target_path}' moved to '{new_path}'!")
    else:
        messagebox.showerror("Error",
                             f"File/Folder '{target_path}' does not exist!")


# Function to update add_menu options
def update_add_menu(*args):
    global add_var, add_menu, edit_menu, move_menu
    if add_var.get() == "FOLDER":
        add_menu["menu"].delete(0, "end")
        add_menu["menu"].add_command(
            label="FOLDER",
            command=lambda: add_var.set("FOLDER"))
        add_menu["menu"].add_command(
            label="FILE",
            command=lambda: add_var.set("FILE"))
        add_var.set("FOLDER")
    else:
        add_menu["menu"].delete(0, "end")
        add_menu["menu"].add_command(
            label="FILE",
            command=lambda: add_var.set("FILE"))
        add_menu["menu"].add_command(
            label="FOLDER",
            command=lambda: add_var.set("FOLDER"))
        add_var.set("FILE")


# Function to update delete_menu options
def update_delete_menu(*args):
    global add_var, delete_menu, edit_menu, move_menu, add_menu, delete_var
    if delete_var.get() == "FOLDER":
        delete_menu["menu"].delete(0, "end")
        delete_menu["menu"].add_command(
            label="FOLDER",
            command=lambda: add_var.set("FOLDER"))
        delete_menu["menu"].add_command(
            label="FILE",
            command=lambda: add_var.set("FILE"))
        add_var.set("FOLDER")
    else:
        delete_menu["menu"].delete(0, "end")
        delete_menu["menu"].add_command(
            label="FILE",
            command=lambda: add_var.set("FILE"))
        delete_menu["menu"].add_command(
            label="FOLDER",
            command=lambda: add_var.set("FOLDER"))
        add_var.set("FILE")


# Function to create the GUI
def create_gui():
    global entry_path, entry_name, move_var, add_var, delete_menu, edit_menu, move_menu, delete_var, add_menu

    def on_add_click():
        action = add_var.get()
        path = entry_path.get()
        name = entry_name.get()
        create_file_or_folder(action, path, name)
        entry_name.delete(0, tk.END)  # Clear the name entry field

    def on_delete_click():
        action = delete_var.get()
        path = entry_path.get()
        name = entry_name.get()
        delete_file_or_folder(action, path, name)
        entry_name.delete(0, tk.END)  # Clear the name entry field

    def on_edit_click():
        path = entry_path.get()
        edit_type = edit_var.get()
        text = text_edit.get("1.0", tk.END)
        edit_file_content(path, edit_type, text)
        entry_name.delete(0, tk.END)  # Clear the name entry field

    def on_edit_select(*args):
        if edit_var.get() == "None":
            text_edit.pack_forget()
        else: 
            text_edit.pack()

    def on_move_click():
        path = entry_path.get()
        new_directory = move_var.get()
        move_file_or_folder(path, new_directory)
        entry_name.delete(0, tk.END)  # Clear the name entry field
        move_var.set("")  # Reset the move directory to default

    root = tk.Tk()
    root.title("DirDynamo")

    style = ttk.Style()
    style.configure("TButton", padding=10, font=("Arial", 10))
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))

    add_var = tk.StringVar()
    delete_var = tk.StringVar()
    edit_var = tk.StringVar()
    edit_var.set("None")  # Default to no edit option selected
    move_var = tk.StringVar()

    frame = ttk.Frame(root, padding=20)
    frame.pack()

    label_path = ttk.Label(frame, text="Directory:")
    label_path.grid(row=0, column=0, sticky="w")

    entry_path = ttk.Entry(frame, width=50)
    entry_path.grid(row=0, column=1, padx=10, pady=5)

    browse_button = ttk.Button(frame, text="Browse", command=browse_directory)
    browse_button.grid(row=0, column=2, padx=10, pady=5)

    label_name = ttk.Label(frame, text="Name:")
    label_name.grid(row=1, column=0, sticky="w")

    entry_name = ttk.Entry(frame, width=50)
    entry_name.grid(row=1, column=1, padx=10, pady=5)

    add_button = ttk.Button(frame, text="Add", command=on_add_click)
    add_button.grid(row=2, column=0, padx=10, pady=5)

    delete_button = ttk.Button(frame, text="Delete", command=on_delete_click)
    delete_button.grid(row=2, column=1, padx=10, pady=5)

    add_menu = ttk.OptionMenu(frame, add_var, "FILE", "FOLDER",
                              command=update_add_menu)
    add_menu.grid(row=2, column=2, padx=10, pady=5)

    delete_menu = ttk.OptionMenu(frame, delete_var, "FILE", "FOLDER",
                                 command=update_delete_menu)
    delete_menu.grid(row=2, column=3, padx=10, pady=5)

    label_edit = ttk.Label(frame, text="Edit Type:")
    label_edit.grid(row=3, column=0, sticky="w")

    edit_menu = ttk.OptionMenu(frame,
                               edit_var,
                               "None",
                               "Append",
                               "Replace",
                               command=on_edit_select)
    edit_menu.grid(row=3, column=1, padx=10, pady=5)

    text_edit = tk.Text(frame, height=10, width=50)
    text_edit.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

    edit_button = ttk.Button(frame, text="Edit", command=on_edit_click)
    edit_button.grid(row=5, column=0, padx=10, pady=5)

    label_move = ttk.Label(frame, text="Move to:")
    label_move.grid(row=6, column=0, sticky="w")

    entry_move = ttk.Entry(frame, textvariable=move_var, width=50)
    entry_move.grid(row=6, column=1, padx=10, pady=5)

    browse_move_button = ttk.Button(frame,
                                    text="Browse",
                                    command=browse_directory_move)
    browse_move_button.grid(row=6, column=2, padx=10, pady=5)

    move_button = ttk.Button(frame, text="Move", command=on_move_click)
    move_button.grid(row=6, column=3, padx=10, pady=5)

    root.mainloop()


# Run the GUI
if __name__ == "__main__":
    create_gui()
