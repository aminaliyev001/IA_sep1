import calendar
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
import style
def fetch_records(start_date, end_date):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_time, calory,id FROM records
        WHERE user_id=? AND date_time BETWEEN ? AND ?
        ORDER BY date_time DESC
    """, (userid, start_date, end_date))
    records = cursor.fetchall()
    conn.close()
    return records

def delete_record_by_id(record_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

def delete_record(event):
    selected_item = records_tree.selection()
    if selected_item:
        record_id = records_tree.item(selected_item, "text")
        if record_id:
            delete_record_by_id(record_id) 
            update_records_tree(records_tree, start_date_picker.get_date(), end_date_picker.get_date())

def update_records_tree(records_tree, start_date, end_date):
    records = fetch_records(start_date, end_date)
    records_tree.delete(*records_tree.get_children())
    total_burned = 0
    total_gained = 0
    
    for record in records:
        date_time_string = record[0]
        date_time_without_milliseconds = date_time_string.split('.')[0] 
        date_time = datetime.strptime(date_time_without_milliseconds, '%Y-%m-%d %H:%M:%S')
        calory = record[1]
        record_id = record[2]
        formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
        if calory < 0:
            total_burned -= calory
            records_tree.insert("", "end", values=(formatted_date, "", f"{-calory:.2f} kcal", ""), tags=("delete",))
        else:
            total_gained += calory
            records_tree.insert("", "end", values=(formatted_date, f"{calory:.2f} kcal", "", ""), tags=("delete",))
        records_tree.item(records_tree.get_children()[-1], text=record_id)    

    records_tree.tag_configure("delete", background="pink")  
    records_tree.tag_bind("delete", "<Button-1>", delete_record)  
    total_difference = total_gained - total_burned
    records_tree.insert("", "end", values=("Total:", f"{total_gained:.2f} kcal", f"{total_burned:.2f} kcal", f"{total_difference:.2f} kcal"))

def search_records():
    start_date = start_date_picker.get_date()
    end_date = end_date_picker.get_date()
    update_records_tree(records_tree, start_date, end_date)

def back(root,user):
    from dashboard import create_dashboard_page
    root.destroy()
    create_dashboard_page(user)

def create_records_page(user):
    global userid,start_date_picker,end_date_picker,records_tree
    userid = user["id"]
    root = tk.Tk()
    root.title("My Records")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (style.WINDOW_WIDTH/2)
    y = (screen_height/2) - (style.WINDOW_HEIGHT/2)

    root.geometry('%dx%d+%d+%d' % (style.WINDOW_WIDTH, style.WINDOW_HEIGHT, x, y))
    root.configure(bg=style.WINDOW_BACKGROUND)

    date_frame = tk.Frame(root, bg=style.WINDOW_BACKGROUND)
    date_frame.pack(side="top", padx=20, pady=20)
    
    start_date_label = tk.Label(date_frame, text="Start Date:", bg=style.WINDOW_BACKGROUND)
    start_date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    start_date_picker = DateEntry(date_frame, date_pattern="yyyy-mm-dd")
    start_date_picker.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    end_date_label = tk.Label(date_frame, text="End Date:", bg=style.WINDOW_BACKGROUND)
    end_date_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    end_date_picker = DateEntry(date_frame, date_pattern="yyyy-mm-dd")
    end_date_picker.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    search_button = tk.Button(date_frame, text="Search", command=search_records)
    search_button.grid(row=0, column=4, pady=5, columnspan=2, sticky="w")

    warning_label = tk.Label(root, text="Click row to delete the record", fg="red")
    warning_label.pack(side="top", padx=20, pady=10)

    records_tree = ttk.Treeview(date_frame, columns=("Date/Time", "Gained", "Burned", "Difference"))
    records_tree.column("#0", width=0)
    records_tree.heading("#1", text="Date/Time")
    records_tree.heading("#2", text="Gained")
    records_tree.heading("#3", text="Burned")
    records_tree.heading("#4", text="Difference")
    records_tree.grid(row=2, columnspan=4, padx=20, pady=(0, 10))

    current_date = datetime.now()
    first_day = datetime(current_date.year, current_date.month, 1)
    _, last_day = calendar.monthrange(current_date.year, current_date.month)
    last_day = datetime(current_date.year, current_date.month, last_day)

    update_records_tree(records_tree, first_day, last_day)
    back_button = tk.Button(root, text="Back to Dashboard", command=lambda: back(root,user))
    back_button.pack(side="bottom", padx=20, pady=10)

    root.mainloop()