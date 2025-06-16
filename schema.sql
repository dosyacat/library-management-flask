-- Create Books table
CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    genre TEXT,
    published_year INTEGER,
    copies_available INTEGER
);

-- Create Members table
CREATE TABLE Members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    membership_date DATE
);

-- Create Loans table
CREATE TABLE Loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    loan_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

-- data.sql

-- Insert into Books
INSERT INTO Books (title, author, genre, published_year, copies_available) VALUES
('1984', 'George Orwell', 'Dystopian', 1949, 3),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 1925, 2),
('To Kill a Mockingbird', 'Harper Lee', 'Classic', 1960, 4),
('Sapiens', 'Yuval Noah Harari', 'Non-Fiction', 2011, 5);

-- Insert into Members
INSERT INTO Members (name, email, membership_date) VALUES
('Alice Smith', 'alice@example.com', '2023-01-15'),
('Bob Johnson', 'bob@example.com', '2022-11-20'),
('Charlie Lee', 'charlie@example.com', '2023-03-01');

-- Insert into Loans
INSERT INTO Loans (book_id, member_id, loan_date, return_date) VALUES
(1, 1, '2023-08-01', NULL),
(2, 2, '2023-07-20', '2023-08-01'),
(3, 3, '2023-08-05', NULL);

-- queries.sql

-- 1. Total available books by genre
SELECT genre, SUM(copies_available) AS total_available
FROM Books
GROUP BY genre;

-- 2. Most borrowed books
SELECT b.title, COUNT(*) AS times_borrowed
FROM Loans l
JOIN Books b ON l.book_id = b.book_id
GROUP BY b.title
ORDER BY times_borrowed DESC;

-- 3. Active loans (not returned)
SELECT l.loan_id, m.name AS member, b.title, l.loan_date
FROM Loans l
JOIN Members m ON l.member_id = m.member_id
JOIN Books b ON l.book_id = b.book_id
WHERE l.return_date IS NULL;

-- 4. Members with most loans
SELECT m.name, COUNT(*) AS total_loans
FROM Loans l
JOIN Members m ON l.member_id = m.member_id
GROUP BY m.name
ORDER BY total_loans DESC;

-- 5. Loans by month
SELECT strftime('%Y-%m', loan_date) AS month, COUNT(*) AS loan_count
FROM Loans
GROUP BY month
ORDER BY month;