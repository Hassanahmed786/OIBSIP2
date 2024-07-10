import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

try:
    user_data = pd.read_csv("bmi_data.csv")
except FileNotFoundError:
    user_data = pd.DataFrame(columns=["Name", "Height (cm)", "Weight (kg)", "BMI", "Category", "Date"])

class BMICalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("400x500")
        self.create_widgets()
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10 10 10 10")
        self.frame.pack(fill="both", expand=True)
        
        self.name_label = ttk.Label(self.frame, text="Name")
        self.name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.frame, width=25)
        self.name_entry.grid(column=1, row=0, padx=5, pady=5)

        self.height_label = ttk.Label(self.frame, text="Height (cm)")
        self.height_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.height_entry = ttk.Entry(self.frame, width=25)
        self.height_entry.grid(column=1, row=1, padx=5, pady=5)

        self.weight_label = ttk.Label(self.frame, text="Weight (kg)")
        self.weight_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.weight_entry = ttk.Entry(self.frame, width=25)
        self.weight_entry.grid(column=1, row=2, padx=5, pady=5)

        self.calc_button = ttk.Button(self.frame, text="Calculate BMI", command=self.calculate_bmi)
        self.calc_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.frame, text="View Historical Data", command=self.view_data)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.plot_button = ttk.Button(self.frame, text="Plot BMI Trends", command=self.plot_bmi_trends)
        self.plot_button.grid(column=0, row=5, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.frame, text="", foreground="blue")
        self.result_label.grid(column=0, row=6, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            name = self.name_entry.get()
            height = float(self.height_entry.get()) / 100  
            weight = float(self.weight_entry.get())
            bmi = weight / (height ** 2)
            category = self.categorize_bmi(bmi)

            self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")

            self.save_data(name, height * 100, weight, bmi, category)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid height and weight.")

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def save_data(self, name, height, weight, bmi, category):
        global user_data
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame([[name, height, weight, bmi, category, date]], columns=user_data.columns)
        user_data = pd.concat([user_data, new_data], ignore_index=True)
        user_data.to_csv("bmi_data.csv", index=False)
        messagebox.showinfo("Data Saved", "Your BMI data has been saved successfully.")

    def view_data(self):
        global user_data
        if user_data.empty:
            messagebox.showinfo("No Data", "No historical data found.")
            return

        top = tk.Toplevel(self)
        top.title("Historical Data")

        data_text = tk.Text(top, wrap="word")
        data_text.pack(expand=True, fill="both")

        data_text.insert("1.0", user_data.to_string(index=False))

    def plot_bmi_trends(self):
        global user_data
        if user_data.empty:
            messagebox.showinfo("No Data", "No historical data found.")
            return

        user_data["Date"] = pd.to_datetime(user_data["Date"])
        user_data.set_index("Date", inplace=True)
        user_data.groupby("Name")["BMI"].plot(legend=True)
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.title("BMI Trends Over Time")
        plt.show()

if __name__ == "__main__":
    app = BMICalculator()
    app.mainloop()
