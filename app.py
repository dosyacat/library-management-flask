from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your own random string

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# ------------------- Books -------------------

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = get_db_connection()
    # Edit book (update)
    if request.method == 'POST' and 'edit_book_id' in request.form:
        book_id = request.form['edit_book_id']
        title = request.form['edit_title']
        author = request.form['edit_author']
        genre = request.form['edit_genre']
        year = request.form['edit_year']
        copies = request.form['edit_copies']
        conn.execute(
            'UPDATE Books SET title=?, author=?, genre=?, published_year=?, copies_available=? WHERE book_id=?',
            (title, author, genre, year, copies, book_id)
        )
        conn.commit()
        flash(f'Book "{title}" updated successfully!')
    # Add book (insert)
    elif request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        copies = request.form['copies']
        conn.execute(
            'INSERT INTO Books (title, author, genre, published_year, copies_available) VALUES (?, ?, ?, ?, ?)',
            (title, author, genre, year, copies)
        )
        conn.commit()
        flash(f'Book "{title}" added successfully!')
    # Search
    search = request.args.get('search', '').strip()
    if search:
        books = conn.execute(
            'SELECT * FROM Books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?',
            (f'%{search}%', f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        books = conn.execute('SELECT * FROM Books').fetchall()
    conn.close()
    return render_template('books.html', books=books, search=search)


@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    conn = get_db_connection()
    active_loans = conn.execute(
        'SELECT COUNT(*) FROM Loans WHERE book_id = ? AND return_date IS NULL', (book_id,)
    ).fetchone()[0]
    if active_loans > 0:
        flash('Cannot delete book: it is currently on loan!')
        conn.close()
        return redirect(url_for('books'))
    conn.execute('DELETE FROM Books WHERE book_id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash('Book deleted successfully.')
    return redirect(url_for('books'))

# ------------------- Members -------------------

@app.route('/members', methods=['GET', 'POST'])
def members():
    conn = get_db_connection()
    # Edit member (update)
    if request.method == 'POST' and 'edit_member_id' in request.form:
        member_id = request.form['edit_member_id']
        name = request.form['edit_name']
        email = request.form['edit_email']
        membership_date = request.form['edit_membership_date']
        conn.execute(
            'UPDATE Members SET name=?, email=?, membership_date=? WHERE member_id=?',
            (name, email, membership_date, member_id)
        )
        conn.commit()
        flash(f'Member "{name}" updated successfully!')
    # Add member (insert)
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        membership_date = request.form['membership_date']
        conn.execute(
            'INSERT INTO Members (name, email, membership_date) VALUES (?, ?, ?)',
            (name, email, membership_date)
        )
        conn.commit()
        flash(f'Member "{name}" added successfully!')
    # Search
    search = request.args.get('search', '').strip()
    if search:
        members = conn.execute(
            'SELECT * FROM Members WHERE name LIKE ? OR email LIKE ?',
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        members = conn.execute('SELECT * FROM Members').fetchall()
    conn.close()
    return render_template('members.html', members=members, search=search)


@app.route('/delete_member/<int:member_id>')
def delete_member(member_id):
    conn = get_db_connection()
    active_loans = conn.execute(
        'SELECT COUNT(*) FROM Loans WHERE member_id = ? AND return_date IS NULL', (member_id,)
    ).fetchone()[0]
    if active_loans > 0:
        flash('Cannot delete member: they have active loans!')
        conn.close()
        return redirect(url_for('members'))
    conn.execute('DELETE FROM Members WHERE member_id = ?', (member_id,))
    conn.commit()
    conn.close()
    flash('Member deleted successfully.')
    return redirect(url_for('members'))

# ----------- Member Loan History & Loan Book to Member -----------

@app.route('/member/<int:member_id>', methods=['GET', 'POST'])
def member_loans(member_id):
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM Members WHERE member_id = ?', (member_id,)).fetchone()
    search_book = request.args.get('search_book', '').strip()
    if search_book:
        books = conn.execute(
            "SELECT book_id, title FROM Books WHERE copies_available > 0 AND (title LIKE ? OR author LIKE ? OR genre LIKE ?)",
            (f'%{search_book}%', f'%{search_book}%', f'%{search_book}%')
        ).fetchall()
    else:
        books = conn.execute('SELECT book_id, title FROM Books WHERE copies_available > 0').fetchall()
    if request.method == 'POST':
        book_id = request.form['book_id']
        loan_date = date.today().isoformat()
        conn.execute('INSERT INTO Loans (book_id, member_id, loan_date, return_date) VALUES (?, ?, ?, NULL)',
                     (book_id, member_id, loan_date))
        conn.execute('UPDATE Books SET copies_available = copies_available - 1 WHERE book_id = ?', (book_id,))
        conn.commit()
        flash(f'Book loaned to {member["name"]}!')
    loans = conn.execute(
        '''
        SELECT l.loan_id, b.title, l.loan_date, l.return_date
        FROM Loans l
        JOIN Books b ON l.book_id = b.book_id
        WHERE l.member_id = ?
        ORDER BY l.loan_date DESC
        ''', (member_id,)
    ).fetchall()
    conn.close()
    return render_template('member_loans.html', member=member, loans=loans, books=books, search_book=search_book)

# ------------------- Loans -------------------

@app.route('/loans', methods=['GET', 'POST'])
def loans():
    conn = get_db_connection()
    members = conn.execute('SELECT member_id, name FROM Members').fetchall()
    search_book = request.args.get('search_book', '').strip()
    if search_book:
        books = conn.execute(
            "SELECT book_id, title FROM Books WHERE copies_available > 0 AND (title LIKE ? OR author LIKE ? OR genre LIKE ?)",
            (f'%{search_book}%', f'%{search_book}%', f'%{search_book}%')
        ).fetchall()
    else:
        books = conn.execute('SELECT book_id, title FROM Books WHERE copies_available > 0').fetchall()
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_id = request.form['book_id']
        loan_date = date.today().isoformat()
        conn.execute('INSERT INTO Loans (book_id, member_id, loan_date, return_date) VALUES (?, ?, ?, NULL)',
                     (book_id, member_id, loan_date))
        conn.execute('UPDATE Books SET copies_available = copies_available - 1 WHERE book_id = ?', (book_id,))
        conn.commit()
        flash('Book loaned successfully!')
    loans = conn.execute(
        '''
        SELECT l.loan_id, m.name AS member, b.title AS book, l.loan_date, l.return_date
        FROM Loans l
        JOIN Members m ON l.member_id = m.member_id
        JOIN Books b ON l.book_id = b.book_id
        ORDER BY l.loan_date DESC
        '''
    ).fetchall()
    conn.close()
    return render_template('loans.html', loans=loans, members=members, books=books, search_book=search_book)

@app.route('/return_loan/<int:loan_id>')
def return_loan(loan_id):
    conn = get_db_connection()
    loan = conn.execute('SELECT book_id, member_id FROM Loans WHERE loan_id = ?', (loan_id,)).fetchone()
    if loan:
        conn.execute('UPDATE Loans SET return_date = ? WHERE loan_id = ?', (date.today().isoformat(), loan_id))
        conn.execute('UPDATE Books SET copies_available = copies_available + 1 WHERE book_id = ?', (loan['book_id'],))
        conn.commit()
        flash('Book returned successfully!')
    conn.close()
    from_member = request.args.get('from_member')
    if from_member:
        return redirect(f'/member/{from_member}')
    return redirect('/loans')

if __name__ == '__main__':
    app.run(debug=True)
