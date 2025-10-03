"""
Expense Tracker with Monthly View + Charts + Color Coding + Date Fix
Author: Jamie Nicole Benwick
Version: 10/2025
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import calendar

EXPENSES_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Utilities", "Shopping", "Entertainment", "Other"]


# --------- Data Handling ---------
def load_exp_list():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as f:
            return json.load(f)
    return []


def save_exp_list(data):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --------- Main App ---------
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.style = tb.Style("flatly")  # modern theme

        # Data
        self.exp_list = load_exp_list()
        self.filt_exp_list = []
        self.sel_idx = None

        now = datetime.now()
        self.curr_month = now.month
        self.curr_year = now.year

        # Setup UI
        self.setup_widgets()
        self.show_current_month()

    def setup_widgets(self):
        # Input Frame
        inp_frame = ttk.LabelFrame(self.root, text="Add / Edit Expense")
        inp_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(inp_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.dt_ent = ttk.Entry(inp_frame)
        self.dt_ent.grid(row=0, column=1, padx=5, pady=5)
        self.dt_ent.insert(0, datetime.today().strftime("%Y-%m-%d"))  # default today

        ttk.Label(inp_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.cat_var = tk.StringVar()
        self.cat_drop = ttk.Combobox(inp_frame, textvariable=self.cat_var, values=CATEGORIES, state="readonly")
        self.cat_drop.grid(row=0, column=3, padx=5, pady=5)
        self.cat_drop.current(0)

        ttk.Label(inp_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.desc_ent = ttk.Entry(inp_frame, width=40)
        self.desc_ent.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        ttk.Label(inp_frame, text="Amount (₱):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amt_ent = ttk.Entry(inp_frame)
        self.amt_ent.grid(row=2, column=1, padx=5, pady=5)

        self.add_btn = ttk.Button(inp_frame, text="Add Expense", command=self.add_exps, bootstyle=SUCCESS)
        self.add_btn.grid(row=2, column=2, pady=5)

        self.upd_btn = ttk.Button(inp_frame, text="Update Selected", command=self.mod_exps, bootstyle=INFO)
        self.upd_btn.grid(row=2, column=3, pady=5)

        self.del_btn = ttk.Button(inp_frame, text="Delete Selected", command=self.del_exps, bootstyle=DANGER)
        self.del_btn.grid(row=2, column=4, padx=5, pady=5)

        # Month Navigation
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(padx=10, pady=5, fill="x")

        self.prev_btn = ttk.Button(nav_frame, text="◀ Prev Month", command=self.prev_month, bootstyle=SECONDARY)
        self.prev_btn.pack(side="left", padx=5)

        self.month_lbl = ttk.Label(nav_frame, text="", font=("Arial", 12, "bold"))
        self.month_lbl.pack(side="left", expand=True)

        self.next_btn = ttk.Button(nav_frame, text="Next Month ▶", command=self.next_month, bootstyle=SECONDARY)
        self.next_btn.pack(side="right", padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("Date", "Category", "Description", "Amount"), show="headings", height=12)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Total
        self.total_lbl = ttk.Label(self.root, text="", font=("Arial", 12))
        self.total_lbl.pack(pady=5)

        # Buttons for charts & all-time view
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Show Pie Chart", command=self.show_pie, bootstyle=PRIMARY).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Show Bar Chart", command=self.show_bar, bootstyle=PRIMARY).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="View All-Time Expenses", command=self.show_all_time, bootstyle=WARNING).pack(side="left", padx=5)

    # ---------- Date Validation ----------
    def validate_date(self, date_str):
        # If empty, use today's date
        if not date_str.strip():
            return datetime.today().strftime("%Y-%m-%d")
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            try:
                year, month, day = map(int, date_str.split("-"))
                last_day = calendar.monthrange(year, month)[1]
                corrected = datetime(year, month, min(day, last_day))
                messagebox.showinfo("Date corrected", f"Adjusted to {corrected.strftime('%Y-%m-%d')}")
                return corrected.strftime("%Y-%m-%d")
            except Exception:
                messagebox.showerror("Invalid Date", "Please enter date as YYYY-MM-DD")
                return None

    # ---------- Core Functions ----------
    def show_current_month(self):
        self.filter_by_month(self.curr_month, self.curr_year)

    def prev_month(self):
        if self.curr_month == 1:
            self.curr_month = 12
            self.curr_year -= 1
        else:
            self.curr_month -= 1
        self.filter_by_month(self.curr_month, self.curr_year)

    def next_month(self):
        if self.curr_month == 12:
            self.curr_month = 1
            self.curr_year += 1
        else:
            self.curr_month += 1
        self.filter_by_month(self.curr_month, self.curr_year)

    def filter_by_month(self, month, year):
        self.filt_exp_list = [ex for ex in self.exp_list if datetime.strptime(ex["date"], "%Y-%m-%d").month == month
                              and datetime.strptime(ex["date"], "%Y-%m-%d").year == year]
        self.refresh_table()
        self.month_lbl.config(text=f"{datetime(year, month, 1).strftime('%B %Y')}")

    def show_all_time(self):
        self.filt_exp_list = self.exp_list[:]
        self.refresh_table()
        self.month_lbl.config(text="All-Time Expenses")

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        total = 0
        for ex in self.filt_exp_list:
            self.tree.insert("", "end", values=(ex["date"], ex["category"], ex["description"], f"₱{ex['amount']:.2f}"), tags=(ex["category"],))
            total += ex["amount"]
        self.total_lbl.config(text=f"Total: ₱{total:.2f}")
        self.color_code_rows()

    def color_code_rows(self):
        colors = {
            "Food": {"bg": "#d4edda", "fg": "#155724"},          # greenish
            "Transport": {"bg": "#d1ecf1", "fg": "#0c5460"},     # light blue
            "Utilities": {"bg": "#fff3cd", "fg": "#856404"},     # yellow
            "Shopping": {"bg": "#e2e3e5", "fg": "#383d41"},      # gray
            "Entertainment": {"bg": "#f8d7da", "fg": "#721c24"}, # red
            "Other": {"bg": "#fefefe", "fg": "#333333"}          # neutral
        }
        for cat, style in colors.items():
            self.tree.tag_configure(cat, background=style["bg"], foreground=style["fg"])

    # ---------- CRUD ----------
    def add_exps(self):
        try:
            dt = self.validate_date(self.dt_ent.get())
            if dt is None:
                return
            cat = self.cat_var.get()
            desc = self.desc_ent.get().strip()
            amt = float(self.amt_ent.get())
            if not desc:
                raise ValueError("Description required")
            self.exp_list.append({"date": dt, "category": cat, "description": desc, "amount": amt})
            save_exp_list(self.exp_list)
            self.show_current_month()
            self.clear_inputs()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid data (e.g. YYYY-MM-DD for date, number for amount)")

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            self.sel_idx = idx
            ex = self.filt_exp_list[idx]

            self.dt_ent.delete(0, tk.END)
            self.dt_ent.insert(0, ex["date"])
            self.cat_var.set(ex["category"])
            self.desc_ent.delete(0, tk.END)
            self.desc_ent.insert(0, ex["description"])
            self.amt_ent.delete(0, tk.END)
            self.amt_ent.insert(0, str(ex["amount"]))

    def mod_exps(self):
        if self.sel_idx is None:
            messagebox.showwarning("No selection", "Please select an expense to update.")
            return
        try:
            dt = self.validate_date(self.dt_ent.get())
            if dt is None:
                return
            cat = self.cat_var.get()
            desc = self.desc_ent.get().strip()
            amt = float(self.amt_ent.get())

            full_idx = self.exp_list.index(self.filt_exp_list[self.sel_idx])
            self.exp_list[full_idx] = {"date": dt, "category": cat, "description": desc, "amount": amt}
            save_exp_list(self.exp_list)
            self.show_current_month()
            self.clear_inputs()
            self.sel_idx = None
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid data (e.g. YYYY-MM-DD for date, number for amount)")

    def del_exps(self):
        if self.sel_idx is None:
            messagebox.showwarning("No selection", "Please select an expense to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?")
        if confirm:
            del self.exp_list[self.exp_list.index(self.filt_exp_list[self.sel_idx])]
            save_exp_list(self.exp_list)
            self.show_current_month()
            self.clear_inputs()
            self.sel_idx = None

    def clear_inputs(self):
        self.dt_ent.delete(0, tk.END)
        self.dt_ent.insert(0, datetime.today().strftime("%Y-%m-%d"))  # reset default
        self.desc_ent.delete(0, tk.END)
        self.amt_ent.delete(0, tk.END)
        self.cat_drop.current(0)

    # ---------- Charts ----------
    def show_pie(self):
        if not self.filt_exp_list:
            messagebox.showinfo("No Data", "No expenses for this period.")
            return
        cat_totals = defaultdict(float)
        for ex in self.filt_exp_list:
            cat_totals[ex["category"]] += ex["amount"]

        plt.figure(figsize=(6, 6))
        plt.pie(cat_totals.values(), labels=cat_totals.keys(), autopct="%.1f%%", startangle=140)
        plt.title("Expenses Breakdown (Pie Chart)")
        plt.show()

    def show_bar(self):
        if not self.filt_exp_list:
            messagebox.showinfo("No Data", "No expenses for this period.")
            return
        cat_totals = defaultdict(float)
        for ex in self.filt_exp_list:
            cat_totals[ex["category"]] += ex["amount"]

        plt.figure(figsize=(8, 5))
        plt.bar(cat_totals.keys(), cat_totals.values())
        plt.title("Expenses Breakdown (Bar Chart)")
        plt.ylabel("Amount (₱)")
        plt.show()


# --------- Run ---------
if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = ExpenseTracker(root)
    root.mainloop()
