import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import sqlite3

# DATABASE

conn = sqlite3.connect("event.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS events(
    name TEXT,
    date TEXT,
    seats INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    name TEXT,
    event TEXT
)
""")

conn.commit()

# COLORS

bg_color = "#f4f6f8"
card_color = "white"
blue = "#2563eb"
light_blue = "#dbeafe"
border = "#cbd5e1"
input_bg = "#f9fafb"

# FUNCTIONS

def update_events():

    cur.execute("SELECT name FROM events")

    data = cur.fetchall()

    event_list = []

    for i in data:
        event_list.append(i[0])

    student_event["values"] = event_list


def add_event():

    name = event_name.get().strip()
    date = event_date.get().strip()
    seats = event_seats.get().strip()

    if name == "" or date == "" or seats == "":
        messagebox.showwarning("Error", "Fill all fields")
        return

    # EVENT NAME VALIDATION

    clean_event = name.replace(" ", "").replace(".", "")

    if clean_event == "":
        messagebox.showwarning(
            "Error",
            "Enter valid event name"
        )
        return

    if not clean_event.isalpha():
        messagebox.showwarning(
            "Error",
            "Enter valid event name"
        )
        return

    # SEATS VALIDATION

       # SEATS VALIDATION

    if not seats.isdigit():
        messagebox.showwarning(
            "Error",
            "Seats should be numbers only"
        )
        return

    seat_count = int(seats)

    if seat_count <= 0:
        messagebox.showwarning(
            "Error",
            "Seats should be greater than 0"
        )
        return

    if seat_count > 1000:
        messagebox.showwarning(
            "Error",
            "Maximum seats allowed is 1000"
        )
        return

    # DATE VALIDATION

    try:

        entered_date = datetime.strptime(
            date,
            "%d-%m-%Y"
        )

        today = datetime.today().date()

        max_date = datetime(
            today.year + 1,
            today.month,
            today.day
        ).date()

        if entered_date.date() < today:

            messagebox.showwarning(
                "Error",
                "Past dates not allowed"
            )
            return

        if entered_date.date() > max_date:

            messagebox.showwarning(
                "Error",
                "Only next 1 year events allowed"
            )
            return

    except:

        messagebox.showwarning(
            "Error",
            "Invalid date"
        )
        return

    # DUPLICATE EVENT CHECK

    cur.execute(
        "SELECT * FROM events WHERE name=?",
        (name,)
    )

    if cur.fetchone():

        messagebox.showwarning(
            "Error",
            "Event already exists"
        )
        return

    # INSERT EVENT

    cur.execute(
        "INSERT INTO events VALUES(?,?,?)",
        (name, date, seats)
    )

    conn.commit()

    event_name.delete(0, tk.END)
    event_date.delete(0, tk.END)
    event_seats.delete(0, tk.END)

    update_events()

    messagebox.showinfo(
        "Success",
        "Event Added"
    )


def view_events():

    output.delete("1.0", tk.END)

    cur.execute("SELECT * FROM events")

    data = cur.fetchall()

    output.insert(
        tk.END,
        "EVENTS\n\n"
    )

    for i in data:

        output.insert(
            tk.END,
            "Event : " + i[0] + "\n"
        )

        output.insert(
            tk.END,
            "Date  : " + i[1] + "\n"
        )

        output.insert(
            tk.END,
            "Seats : " + str(i[2]) + "\n"
        )

        output.insert(
            tk.END,
            "----------------------\n"
        )


def register_student():

    name = student_name.get().strip()
    event = student_event.get().strip()

    if name == "" or event == "":
        messagebox.showwarning(
            "Error",
            "Fill all fields"
        )
        return

    # STUDENT NAME VALIDATION

    clean_name = name.replace(" ", "").replace(".", "")

    if clean_name == "":
        messagebox.showwarning(
            "Error",
            "Enter valid student name"
        )
        return

    if not clean_name.isalpha():
        messagebox.showwarning(
            "Error",
            "Enter valid student name"
        )
        return

    # DUPLICATE REGISTRATION CHECK

    cur.execute(
        "SELECT * FROM students WHERE name=? AND event=?",
        (name, event)
    )

    if cur.fetchone():

        messagebox.showwarning(
            "Error",
            "Student already registered"
        )
        return

    # SEAT CHECKING

    cur.execute(
        "SELECT seats FROM events WHERE name=?",
        (event,)
    )

    total_seats = int(cur.fetchone()[0])

    cur.execute(
        "SELECT COUNT(*) FROM students WHERE event=?",
        (event,)
    )

    registered = cur.fetchone()[0]

    if registered >= total_seats:

        messagebox.showwarning(
            "Error",
            "Seats Full"
        )
        return

    # REGISTER STUDENT

    cur.execute(
        "INSERT INTO students VALUES(?,?)",
        (name, event)
    )

    conn.commit()

    student_name.delete(0, tk.END)

    student_event.set("")

    messagebox.showinfo(
        "Success",
        "Student Registered"
    )


def view_students():

    output.delete("1.0", tk.END)

    cur.execute("SELECT * FROM students")

    data = cur.fetchall()

    output.insert(
        tk.END,
        "PARTICIPANTS\n\n"
    )

    for i in data:

        output.insert(
            tk.END,
            "Student : " + i[0] + "\n"
        )

        output.insert(
            tk.END,
            "Event   : " + i[1] + "\n"
        )

        output.insert(
            tk.END,
            "----------------------\n"
        )


def delete_event():

    name = delete_name.get().strip()

    if name == "":
        messagebox.showwarning(
            "Error",
            "Enter Event Name"
        )
        return

    # CHECK WHETHER EVENT EXISTS
    cur.execute(
        "SELECT * FROM events WHERE name=?",
        (name,)
    )

    if not cur.fetchone():
        messagebox.showwarning(
            "Error",
            "Event Not Found"
        )
        return

    # DELETE EVENT
    cur.execute(
        "DELETE FROM events WHERE name=?",
        (name,)
    )

    # DELETE REGISTERED STUDENTS
    cur.execute(
        "DELETE FROM students WHERE event=?",
        (name,)
    )

    conn.commit()

    delete_name.delete(0, tk.END)

    student_event.set("")

    update_events()

    messagebox.showinfo(
        "Success",
        "Event Deleted Successfully"
    )

# MAIN WINDOW

root = tk.Tk()

root.title("College Event Management")

root.geometry("900x680")

root.configure(bg=bg_color)

# TITLE

title = tk.Label(
    root,
    text="College Event Management System",
    font=("Arial", 20, "bold"),
    bg=bg_color,
    fg="#1f2937"
)

title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Manage Events and Student Registrations",
    font=("Arial", 10),
    bg=bg_color,
    fg="gray"
)

subtitle.pack()

# MAIN FRAME

main_frame = tk.Frame(
    root,
    bg=bg_color
)

main_frame.pack(pady=30)

# ADD EVENT CARD

card1 = tk.Frame(
    main_frame,
    bg=card_color,
    bd=1,
    relief="solid",
    width=320,
    height=340
)

card1.grid(
    row=0,
    column=0,
    padx=25
)

card1.grid_propagate(False)

tk.Label(
    card1,
    text="Add Event",
    font=("Arial", 16, "bold"),
    bg=card_color
).pack(pady=15)

tk.Label(
    card1,
    text="Event Name",
    bg=card_color
).pack()

event_name = tk.Entry(
    card1,
    width=28,
    font=("Arial", 11),
    relief="solid",
    bd=2,
    bg=input_bg,
    highlightbackground=border,
    highlightcolor=blue,
    highlightthickness=1
)

event_name.pack(pady=5)

tk.Label(
    card1,
    text="Date (DD-MM-YYYY)",
    bg=card_color
).pack()

event_date = tk.Entry(
    card1,
    width=28,
    font=("Arial", 11),
    relief="solid",
    bd=2,
    bg=input_bg,
    highlightbackground=border,
    highlightcolor=blue,
    highlightthickness=1
)

event_date.pack(pady=5)

tk.Label(
    card1,
    text="Number of Seats",
    bg=card_color
).pack()

event_seats = tk.Entry(
    card1,
    width=28,
    font=("Arial", 11),
    relief="solid",
    bd=2,
    bg=input_bg,
    highlightbackground=border,
    highlightcolor=blue,
    highlightthickness=1
)

event_seats.pack(pady=5)

tk.Button(
    card1,
    text="Add Event",
    width=20,
    bg=blue,
    fg="white",
    relief="flat",
    command=add_event
).pack(pady=20)

# REGISTER CARD

card2 = tk.Frame(
    main_frame,
    bg=card_color,
    bd=1,
    relief="solid",
    width=320,
    height=340
)

card2.grid(
    row=0,
    column=1,
    padx=25
)

card2.grid_propagate(False)

tk.Label(
    card2,
    text="Register Student",
    font=("Arial", 16, "bold"),
    bg=card_color
).pack(pady=15)

tk.Label(
    card2,
    text="Student Name",
    bg=card_color
).pack()

student_name = tk.Entry(
    card2,
    width=28,
    font=("Arial", 11),
    relief="solid",
    bd=2,
    bg=input_bg,
    highlightbackground=border,
    highlightcolor=blue,
    highlightthickness=1
)

student_name.pack(pady=5)

tk.Label(
    card2,
    text="Select Event",
    bg=card_color
).pack()

student_event = ttk.Combobox(
    card2,
    width=25,
    state="readonly"
)

student_event.pack(pady=5)

tk.Button(
    card2,
    text="Register Student",
    width=20,
    bg=blue,
    fg="white",
    relief="flat",
    command=register_student
).pack(pady=20)

# ACTION BUTTONS

action_frame = tk.Frame(
    root,
    bg=bg_color
)

action_frame.pack(pady=10)

tk.Button(
    action_frame,
    text="View Events",
    width=18,
    bg=light_blue,
    relief="flat",
    command=view_events
).grid(row=0, column=0, padx=10)

tk.Button(
    action_frame,
    text="View Participants",
    width=18,
    bg=light_blue,
    relief="flat",
    command=view_students
).grid(row=0, column=1, padx=10)

delete_name = tk.Entry(
    action_frame,
    width=20,
    font=("Arial", 10),
    relief="solid",
    bd=2,
    bg=input_bg
)

delete_name.grid(
    row=0,
    column=2,
    padx=10
)

tk.Button(
    action_frame,
    text="Delete Event",
    width=15,
    bg="#e5e7eb",
    relief="flat",
    command=delete_event
).grid(row=0, column=3, padx=10)

# OUTPUT BOX

output = tk.Text(
    root,
    height=15,
    width=95,
    font=("Arial", 10)
)

output.pack(pady=25)

# LOAD EVENTS

update_events()

# RUN

root.mainloop()