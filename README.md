# Simple Expense Tracker (v2)

# Simple Expense Tracker (v2)

A desktop expense tracker built with **Python + Tkinter + ttkbootstrap**, designed to make personal budgeting simple but effective.  
This is an improved version of the original [`simple_expense_tracker`](https://github.com/happythursdays/simple_expense_tracker) with added features and a cleaner UI.

---

## ✨ Features

- Add, edit, and delete expenses  
- Categorize expenses (Food, Transport, Utilities, Shopping, Entertainment, Other)  
- Month navigation (◀ Previous / Next ▶)  
- **All-Time Expenses view**  
- **Color-coded categories** in the table for easy scanning  
- **Pie chart & bar chart** visualizations of spending  
- Data persistence via local `expenses.json` file  
- Input exact **date (YYYY-MM-DD)** for flexibility (helpful if you add expenses at the end of the week or month)  
- Default date automatically set to **today** for convenience  

---

## 📊 Comparison to Version 1

| Feature                        | v1 | v2 |
|--------------------------------|----|----|
| Add/Edit/Delete expenses       | ✅ | ✅ |
| Categories                     | ✅ | ✅ |
| Monthly navigation             | ✅ | ✅ |
| Charts (Pie & Bar)             | ✅ | ✅ |
| All-Time view                  | ❌ | ✅ |
| Color-coded categories         | ❌ | ✅ |
| Exact date input               | Limited | ✅ Full support |
| Default today’s date           | ❌ | ✅ |
| UI / Modern theme              | Basic | Polished with **ttkbootstrap** |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/happythursdays/simple_expense_tracker.git
cd simple_expense_tracker
```
### 2. Install dependencies

Make sure you have Python 3.8+ installed. Then:
```
pip install -r requirements.txt

``` 
If you don’t have requirements.txt, manually install:
```bash
pip install ttkbootstrap matplotlib
```
### 3. Run the app
```bash
python v2_expense_tracker.py
```
---

## Screenshots
(to be added)

---

## Data Storage
Expenses are stored locally in expenses.json in the project directory.
Each record has the format:
``` bash
{
  "date": "2025-10-02",
  "category": "Food",
  "description": "Lunch at cafe",
  "amount": 150.0
}
```
---
## Future Plans

- SQL database support (v3, in progress)
- Recurring expenses
- More advanced analytics

---
## Author | Jamie Nicole Benwick
- jamienicolevillelabenwick@gmail.com
- Las Piñas, Metro Manila
