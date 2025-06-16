# 📚 Library Management System

A modern web application to manage a library’s books, members, and loans, built with **Flask** and **SQLite**.  

---

## ✨ Features

- **Books:** Add, edit, delete, and search books.  
- **Members:** Add, edit, delete, and search library members.  
- **Loans:** Loan and return books to members, with book search and availability checks.  
- **Member History:** View a member’s complete loan history.
- **Modals:** All add/edit operations use pop-up modals for a modern UX.
- **Data Safety:** Prevent deleting books or members with active loans.
- **Flash Messages:** See confirmation and error messages for all actions.
- **Search Everywhere:** Search and filter on all main pages.
- **Responsive Design:** Clean look on desktop and mobile.

---

## 🖼️ Screenshots

Screenshots are in Screenshots folder

---

## 🗄️ Database Schema

+---------+      +---------+      +-------+
| Members |      |  Loans  |      | Books |
+---------+      +---------+      +-------+
| member_id <----| member_id|     |book_id|
| name     |     | loan_id  |---->|title  |
| email    |     | book_id  |     |author |
| membership_date| loan_date|     |genre  |
+---------+      |return_date|    |year   |
                 +---------+      |copies |
                                  +-------+

**Main Tables:**
- **Books** (`book_id`, `title`, `author`, `genre`, `published_year`, `copies_available`)
- **Members** (`member_id`, `name`, `email`, `membership_date`)
- **Loans** (`loan_id`, `book_id`, `member_id`, `loan_date`, `return_date`)

---

## 🛠️ Tech Stack

- **Python 3**
- **Flask**
- **SQLite**
- **HTML/CSS**

---

## 🚀 Setup Instructions

1. **Clone this repo and install dependencies:**
    ```sh
    git clone https://github.com/yourusername/library-management-flask.git
    cd library-management-flask
    pip install -r requirements.txt
    ```

2. **Initialize the database and sample data:**
    ```sh
    sqlite3 library.db < schema.sql
    sqlite3 library.db < add_sample_data.sql
    ```

3. **Run the application:**
    ```sh
    python app.py
    ```
    Then visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📦 Sample Data

- The file `add_sample_data.sql` gives you demo books and members for instant testing.
- You can change, extend, or reset as you wish!

---


## 👤 Author

[Yeldos Zhumakyn](https://github.com/dosyacat)  
2025

