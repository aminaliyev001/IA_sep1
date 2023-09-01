from tkinter import messagebox
import sqlite3
from tkinter import *
from datetime import datetime
from tkinter.ttk import Treeview
import style
from PIL import Image, ImageTk
from ask import main
from records import create_records_page
def get_user_by_id(id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE  id=?", (id,))
        user = cursor.fetchone()
        conn.close()
        if user is None:
            return None
        else:
            return {
                "id": user[0],
                "name": user[1],
                "surname": user[2],
                "current_weight": user[3],
                "target_weight": user[4],
                "height": user[5],
                "pin": user[6],
                "email": user[7],
                "password": user[8]
            }

def create_daily_plan_page(user,root):
    def back_to_dashboard():
        daily_plan_window.destroy()
        create_dashboard_page(user)

    root.destroy()
    daily_plan_window = Tk()
    daily_plan_window.title("Daily Plan")
    screen_width = daily_plan_window.winfo_screenwidth()
    screen_height = daily_plan_window.winfo_screenheight()
    x = (screen_width / 2) - (1300 / 2)
    y = (screen_height / 2) - (650 / 2)
    daily_plan_window.geometry('%dx%d+%d+%d' % (1300, 650, x, y))
    daily_plan_window.configure(bg=style.WINDOW_BACKGROUND)

    back_button = Button(daily_plan_window, text="Back to Dashboard", command=back_to_dashboard)
    back_button.pack(side="top", anchor="nw", padx=20, pady=5) 

    header_label = Label(daily_plan_window, text="Your Daily Plan", **style.HEADER_STYLE)
    header_label.pack(pady=(5, 5))
    
    meal_frame = Frame(daily_plan_window, bg=style.WINDOW_BACKGROUND)
    meal_frame.pack(padx=20, pady=10)
    
    meal_label = Label(meal_frame, text="Meal Plan:", **style.LABEL_STYLE)
    meal_label.pack(anchor="w")
    
    meal_plan = [
        {"meal": "Breakfast", "food": "1 boiled egg & 1 tbls 0 fat sour cream & 1 slice whole wheat bread", "drink": "first 1/2 lemon 1 glass water & in the end 1 glass of 0 fat milk", "calories": 240},
        {"meal": "Snack", "food": "Orange or apple or banana", "drink": "2 glasses of water", "calories": 80},
        {"meal": "Lunch", "food": "Vegetable salad or soup with grilled chicken or grilled meat", "drink": "400 ml water (if you eat salad)", "calories": 350},
        {"meal": "Snack", "food": "Kiwi or pineapple or orange or banana", "drink": "2 glasses of water", "calories": 80},
        {"meal": "Dinner(at the latest 6pm)", "food": "1 boiled egg & 2 slices whole wheat bread & 1 tbls 0 fat sour cream & 1 slice 0 fat white cheese", "drink": "400 ml water", "calories": 270}
    ]
    
    meal_tree = Treeview(meal_frame, columns=("Meal", "Food", "Drink", "Calories"), show="headings",height=6)
    meal_tree.heading("Meal", text="Meal")
    meal_tree.heading("Food", text="Food")
    meal_tree.heading("Drink", text="Drink")
    meal_tree.heading("Calories", text="Calories (kcal)")
    meal_tree.column("Food", width=550)
    meal_tree.column("Drink", width=330)
    meal_tree.column("Calories", width=50)
    meal_tree.pack(fill="both", expand=True)
    
    for meal in meal_plan:
        meal_tree.insert("", "end", values=(meal["meal"], meal["food"], meal["drink"], meal["calories"]))
    
    exercise_frame = Frame(daily_plan_window, bg=style.WINDOW_BACKGROUND)
    exercise_frame.pack(padx=20, pady=10)
    
    exercise_label = Label(exercise_frame, text="Exercise Plan:", **style.LABEL_STYLE)
    exercise_label.pack(anchor="w")
    
    exercise_plan = [
        {"time": "7:00 AM - 8:00 AM", "activity": "20 minutes of brisk walking or light jogging & 25 push-ups & 15 minutes of stretching and yoga", "calories": 375},
        {"time": "1:00 PM - 2:00 PM", "activity": "30 minutes of moderate-intensity cardio (e.g., cycling, swimming) & 20 minutes of bodyweight exercises (e.g., squats, lunges)", "calories": 650},
        {"time": "5:00 PM - 6:00 PM", "activity": "25 minutes of brisk walking or light jogging & 25 minutes of strength training & 20 minutes of yoga or relaxation exercises", "calories": 600},
    ]
    
    exercise_tree = Treeview(exercise_frame, columns=("Time", "Activity", "Calories"), show="headings",height=3)
    exercise_tree.heading("Time", text="Time")
    exercise_tree.heading("Activity", text="Activity")
    exercise_tree.heading("Calories", text="Calories Burned")
    exercise_tree.column("Activity", width=700)
    exercise_tree.column("Time", width=130)
    exercise_tree.column("Calories", width=50)
    exercise_tree.pack(fill="both", expand=True)
    
    for exercise in exercise_plan:
        exercise_tree.insert("", "end", values=(exercise["time"], exercise["activity"], exercise["calories"]))
    
    sleep_tips_frame = Frame(daily_plan_window, bg=style.WINDOW_BACKGROUND)
    sleep_tips_frame.pack(padx=20, pady=10)

    sleep_tips_label = Label(sleep_tips_frame, text="Sleep Tips:", **style.LABEL_STYLE)
    sleep_tips_label.pack(anchor="w")

    sleep_tips = [
        {"tip": "Go to bed and wake up at the same time every day, even on weekends.", "time": "10:00 PM - 6:00 AM"},
        {"tip": "Create a relaxing bedtime routine, such as reading or taking a warm bath.", "time": "9:00 PM - 9:45 PM"},
        {"tip": "Keep your bedroom dark, quiet, and cool for better sleep.", "time": "10:00 PM - 6:00 AM"},
        {"tip": "Avoid screens (phones, computers, TVs) at least 1 hour before bed.", "time": "9:00 PM - 10:00 PM"},
        {"tip": "Avoid screens (phones, computers, TVs) at least 1 hour before bed.", "time": "11:00 PM - 7:00 AM & 8:00 AM"},
    ]

    sleep_tips_tree = Treeview(sleep_tips_frame, columns=("Tip", "Recommended Time"), show="headings",height=5)
    sleep_tips_tree.heading("Tip", text="Tip")
    sleep_tips_tree.heading("Recommended Time", text="Recommended Time")
    sleep_tips_tree.column("Recommended Time", width=180)
    sleep_tips_tree.column("Tip", width=450)
    sleep_tips_tree.pack(fill="both", expand=True)

    for tip in sleep_tips:
        sleep_tips_tree.insert("", "end", values=(tip["tip"], tip["time"]))

    daily_plan_window.mainloop()

def edit_profile(root):
    from dashboard import create_dashboard_page
    global user_local
    user_local = get_user_by_id(userid) 
    def back(edit_window,user):
         edit_window.destroy()
         create_dashboard_page(user_local)
    def save_changes():
        global user_local
        new_password = password_entry.get()
        new_current_weight = current_weight_entry.get()
        new_target_weight = target_weight_entry.get()
        new_height = height_entry.get()

        if not new_password or not new_current_weight or not new_target_weight or not new_height:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        try:
            new_current_weight = float(new_current_weight)
            new_target_weight = float(new_target_weight)
            new_height = float(new_height)
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid numeric values.")
            return
        if ((new_target_weight)+1) > (new_current_weight):
            messagebox.showwarning("Warning", "Target weight should be at least 1 kg less than current weight!")
            return
        
        if(len(new_password) < 4):
            messagebox.showwarning("Warning", "Password length less than 4 can be easy to guess your.")
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(""" 
        UPDATE users SET password=?,current_weight=?,target_weight=?,height=? WHERE id=?
        """,(new_password,new_current_weight,new_target_weight,new_height,user_local["id"]))
        conn.commit()
        conn.close()
        user_local = get_user_by_id(userid)
        messagebox.showinfo("Success","Your profile is updated.")
        back(edit_window,user_local)

    root.destroy()
    edit_window = Tk()
    edit_window.title("Edit Profile")
    screen_width = edit_window.winfo_screenwidth()
    screen_height = edit_window.winfo_screenheight()
    x = (screen_width/2) - (style.WINDOW_WIDTH/2)
    y = (screen_height/2) - (style.WINDOW_HEIGHT/2)
    edit_window.geometry('%dx%d+%d+%d' % (style.WINDOW_WIDTH, style.WINDOW_HEIGHT, x, y))
    edit_window.configure(bg=style.WINDOW_BACKGROUND)

    password_label = Label(edit_window, text="Password:", **style.LABEL_STYLE)
    password_label.pack()
    password_entry = Entry(edit_window)
    password_entry.insert(0, user_local["password"]) 
    password_entry.pack()

    current_weight_label = Label(edit_window, text="Current Weight:", **style.LABEL_STYLE)
    current_weight_label.pack()
    current_weight_entry = Entry(edit_window)
    current_weight_entry.insert(0, user_local["current_weight"])  
    current_weight_entry.pack()

    target_weight_label = Label(edit_window, text="Target Weight:", **style.LABEL_STYLE)
    target_weight_label.pack()
    target_weight_entry = Entry(edit_window)
    target_weight_entry.insert(0, user_local["target_weight"])  
    target_weight_entry.pack()

    height_label = Label(edit_window, text="Height:", **style.LABEL_STYLE)
    height_label.pack()
    height_entry = Entry(edit_window)
    height_entry.insert(0, user_local["height"])  
    height_entry.pack()

    save_button = Button(edit_window, text="Save Changes", command=save_changes)
    save_button.pack(pady=10)

    back_button = Button(edit_window, text="Back to Dashboard", command=lambda: back(edit_window,user_local))
    back_button.pack(side="bottom", padx=20, pady=10)

    edit_window.mainloop()

def calculate_sum_kcal():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT calory FROM records WHERE user_id=?", (userid,))
        records = cursor.fetchall()
        total_calories = sum(record[0] for record in records)
        conn.close()
        return total_calories
def records_user(user,root):
     root.destroy()
     create_records_page(user)
def get_bmi_status(bmi):
        if bmi < 16:
            return "Severe Thinness"
        elif bmi < 17:
            return "Moderate Thinness"
        elif bmi < 18.5:
            return "Mild Thinness"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        elif bmi < 35:
            return "Obese Class I"
        elif bmi < 40:
            return "Obese Class II"
        else:
            return "Obese Class III"
def add_calories_burned(calories_gained_entry):
        calories_burned = calories_gained_entry.get()
        try:
            calories_burned = float(calories_burned)
        except ValueError:
            messagebox.showinfo("Error", "Please enter a valid numeric value.")
            return 
    
        if calories_burned <= 0:
            messagebox.showinfo("Error", "Please enter a positive calorie value.")
            return
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (user_id, date_time, calory)
            VALUES (?, ?, ?)
        """, (userid, datetime.now(), -calories_burned))
        conn.commit()
        calories_message_label.config(text="Calories burned added successfully.")
        kcal_to_burn_label.config(text=str(kcal_to_burn+calculate_sum_kcal())+" kcal left 🔥")
        conn.close()
        calories_gained_entry.delete(0,END)
        today_burned_label.config(text=f"Calories Burned Today: {today_burned_func():.2f} kcal")

def add_calories_gained(calories_gained_entry):
        calories_gained = calories_gained_entry.get()
        try:
            calories_gained = float(calories_gained)
        except ValueError:
            messagebox.showinfo("Error", "Please enter a valid numeric value.")
            return
        if calories_gained <= 0:
            messagebox.showinfo("Error", "Please enter a positive calorie value.")
            return
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (user_id, date_time, calory)
            VALUES (?, ?, ?)
        """, (userid, datetime.now(), calories_gained))
        conn.commit()
        conn.close()
        calories_message_label.config(text="Calories gained added successfully.")
        kcal_to_burn_label.config(text=str(kcal_to_burn+calculate_sum_kcal())+" kcal left 🔥")
        calories_gained_entry.delete(0,END)
        today_gained_label.config(text=f"Calories Gained Today: {today_gained_func():.2f} kcal")

     
def today_burned_func():
    today = datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(calory) FROM records
        WHERE user_id = ? AND date_time >= ? AND date_time < ? AND calory < 0;
    """, (userid, today, today + ' 23:59:59'))
    today_burned = abs(cursor.fetchone()[0] or 0.0)  
    conn.close()
    return today_burned

def today_gained_func():
    today = datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(calory) FROM records
        WHERE user_id = ? AND date_time >= ? AND date_time < ? AND calory >= 0;
    """, (userid, today, today + ' 23:59:59'))
    today_gained = cursor.fetchone()[0] or 0.0  
    conn.close()
    return today_gained

def create_dashboard_page(user):
    global kcal_to_burn,calories_message_label,kcal_to_burn_label,userid,today_gained_label,today_burned_label
    userid = user["id"]
    if(user["target_weight"] == None):
            main(userid)
            user = get_user_by_id(userid)
    quotes = [
    "The only bad workout is the one that didn't happen.",
    "Don't wish for it, work for it.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "The only way to achieve your goals is to start, and the only way to start is to stop talking and begin doing.",
    "The future depends on what you do today.",
    "Believe you can and you're halfway there.",
    "It's not about being the best; it's about being better than you were yesterday."
        ]
    root = Tk()
    root.title("Dashboard")
    root.configure(bg=style.WINDOW_BACKGROUND)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (style.WINDOW_WIDTH/2)
    y = (screen_height/2) - (style.WINDOW_HEIGHT/2)
    root.geometry('%dx%d+%d+%d' % (style.WINDOW_WIDTH, style.WINDOW_HEIGHT, x, y))
    root.configure(bg=style.WINDOW_BACKGROUND)

    user_info_frame = Frame(root, bg=style.USER_INFO_BACKGROUND)
    user_info_frame.pack(side="top", fill="x", padx=20, pady=20)

    image = Image.open("user.png")  
    user_icon = ImageTk.PhotoImage(image)

    user_icon_label = Label(user_info_frame, image=user_icon, bg=style.USER_INFO_BACKGROUND)
    user_icon_label.image = user_icon
    user_icon_label.pack(side="left", padx=(0, 20))

    user_info_label = Label(
        user_info_frame, 
        text=f"{user['name']} {user['surname']}",
        bg=style.USER_INFO_BACKGROUND,
        fg=style.USER_INFO_TEXT,
        font=style.LARGE_FONT,
        anchor="w"
    )
    user_info_label.pack(side="left")
    exit_button = Button(user_info_frame, text="Exit", command=root.destroy)
    exit_button.pack(side="right", padx=10)

    edit_profile_button = Button(
        user_info_frame,
        text="Edit Profile",
        command=lambda: edit_profile(root)  
    )
    edit_profile_button.pack(side="right", padx=10)

    records_button = Button(
        user_info_frame,
        text="My records",
        command=lambda: records_user(user,root)  
    )
    records_button.pack(side="right", padx=10)

    suggestion_button = Button(
        user_info_frame,
        text="Suggestions",
        command=lambda: create_daily_plan_page(user,root)  
    )
    suggestion_button.pack(side="right", padx=10)

    quote_frame = Frame(root, bg=style.QUOTE_BACKGROUND)
    quote_frame.pack(side="top", fill="x", padx=20, pady=10)
    current_day = datetime.today().weekday()
    quote_of_the_day = quotes[current_day] 

    quote_label = Label(
    quote_frame,
    text=f"Quote of the day: {quote_of_the_day}",
    bg=style.QUOTE_BACKGROUND,
    fg=style.QUOTE_TEXT,
    font=style.NORMAL_FONT,
    anchor="center"
    )
    quote_label.grid(row=0, column=0, padx=(20, 0), pady=(0, 10),columnspan=2,sticky="we")

    days_left = (float(user["current_weight"]) - float(user["target_weight"]) + (calculate_sum_kcal()/7700)) // 0.1
    average_label = Label(
        quote_frame,
        text=f"{int(days_left)} days left (cutting 700 kcal a day on average)",
        bg=style.QUOTE_BACKGROUND,
        fg=style.QUOTE_TEXT,
        font=style.NORMAL_FONT,
        anchor="center"
    )
    average_label.grid(row=1, column=0, padx=(20, 0),columnspan=2, pady=(0, 10))
    quote_frame.columnconfigure(0, weight=1)
    quote_frame.columnconfigure(1, weight=1)
        
    bmi_frame = Frame(root)
    bmi_frame.pack(padx=20, pady=20)

    height_m = user["height"]  
    bmi = user["current_weight"] / ((height_m/100) ** 2)
    bmi_label = Label(bmi_frame, text=f"Your BMI: {bmi:.2f} ({get_bmi_status(bmi)})")
    bmi_label.pack(pady=10)

    kcal_frame = Frame(root)
    kcal_frame.pack(side="left", padx=20, pady=20)

    kcal_to_burn = (float(user["current_weight"]) - float(user["target_weight"])) * 7700

    kcal_to_burn_label = Label(kcal_frame, text=str(kcal_to_burn + calculate_sum_kcal()) + " kcal left 🔥",font=style.NORMAL_FONT)
    kcal_to_burn_label.grid(row=0, columnspan=2, padx=5, pady=5)

    calories_burned_label = Label(kcal_frame, text="Calories Burned:",font=style.NORMAL_FONT)
    calories_burned_label.grid(row=1, column=0, padx=5, pady=5)
    
    calories_burned_entry = Entry(kcal_frame)
    calories_burned_entry.grid(row=1, column=1, padx=5, pady=5)

    calories_gained_label = Label(kcal_frame, text="Calories Gained:",font=style.NORMAL_FONT)
    calories_gained_label.grid(row=2, column=0, padx=5, pady=5)
    
    calories_gained_entry = Entry(kcal_frame)
    calories_gained_entry.grid(row=2, column=1, padx=5, pady=5)

    add_calories_burned_button = Button(kcal_frame, text="Add Calories Burned", command=lambda:add_calories_burned(calories_burned_entry))
    add_calories_burned_button.grid(row=3, column=0, padx=5, pady=10)

    add_calories_gained_button = Button(kcal_frame, text="Add Calories Gained", command=lambda:add_calories_gained(calories_gained_entry))
    add_calories_gained_button.grid(row=3, column=1, padx=5, pady=10)

    calories_message_label = Label(kcal_frame, text="")
    calories_message_label.grid(row=4, columnspan=2, padx=5, pady=5)

    summary_frame = Frame(root)
    summary_frame.pack(side="right", padx=20, pady=20)
    
    today_summary_label = Label(summary_frame, text="Today's Summary", font=style.MEDIUM_FONT)
    today_summary_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 50))  

    today_burned_label = Label(summary_frame, text=f"Calories Burned Today: {today_burned_func():.2f} kcal", font=style.NORMAL_FONT)
    today_burned_label.grid(row=1, column=0, columnspan=2,padx=10, pady=5)

    today_gained_label = Label(summary_frame, text=f"Calories Gained Today: {today_gained_func():.2f} kcal", font=style.NORMAL_FONT)
    today_gained_label.grid(row=2, column=1, columnspan=2,padx=10, pady=5)

    root.mainloop()