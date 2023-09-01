from tkinter import *
import sqlite3
import style 
from tkinter import messagebox
def main(userid):
    def calculate():
        weight_text = weight_entry.get()
        height_text = height_entry.get()
        target_weight_text = target_weight_entry.get()
        
        if not weight_text or not height_text or not target_weight_text:
            messagebox.showwarning("Fields Empty", "Please fill in all fields.")
            return
        
        try:
            weight = float(weight_text)
            height_cm = float(height_text)
            target_weight = float(target_weight_text)
            
            if (target_weight + 1) > weight:
                messagebox.showwarning("Warning", "Target weight should be at least 1 kg less than current weight!")
            else:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users
                    SET target_weight = ?, current_weight = ?, height = ?
                    WHERE id = ?
                """, (target_weight, weight, height_cm, userid))
                conn.commit()
                conn.close()
                root.destroy()
                
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid numeric values.")
    updated_user = None
    root = Tk()
    root.title("Fill the form")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - style.WINDOW_WIDTH) // 2
    y = (screen_height - style.WINDOW_HEIGHT) // 2
    root.geometry(f"{style.WINDOW_WIDTH}x{style.WINDOW_HEIGHT}+{x}+{y}")

    root.configure(bg=style.WINDOW_BACKGROUND)

    weight_label = Label(root, text="Weight (kg):", **style.LABEL_STYLE)
    weight_label.pack()
    weight_entry = Entry(root)
    weight_entry.pack()

    height_label = Label(root, text="Height (cm):", **style.LABEL_STYLE)
    height_label.pack()
    height_entry = Entry(root)
    height_entry.pack()

    target_weight_label = Label(root, text="Target Weight (kg, 1 kg less than current):", **style.LABEL_STYLE)
    target_weight_label.pack()
    target_weight_entry = Entry(root)
    target_weight_entry.pack()

    save_button = Button(root, text="Save Changes", command=calculate)
    save_button.pack(pady=10)
    root.mainloop()