import mysql.connector as mycon
from datetime import datetime, timedelta


con = mycon.connect(host="localhost", user="root", password="ahsurej", database="jeru")
cur = con.cursor()

cur.execute(
    """
        CREATE TABLE IF NOT EXISTS Books (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            author VARCHAR(100),
            availability_status BOOLEAN default 0
        )
    """
)

cur.execute(
    """
        CREATE TABLE IF NOT EXISTS Members (
            member_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
        )
    """
)
cur.execute(
    """
        CREATE TABLE IF NOT EXISTS Loans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bookid INT,
            memberid INT,
            issue_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            due_date DATETIME DEFAULT(CURRENT_TIMESTAMP + INTERVAL 14 DAY),
            FOREIGN KEY (bookid) REFERENCES Books(book_id),
            FOREIGN KEY (memberid) REFERENCES Members(member_id)
        )
    """
)


def display_all_books():
    cur.execute("SELECT * FROM Books")
    books = cur.fetchall()

    print("Books:")
    print("ID  | Title                 | Author                | Status")
    print("----|-----------------------|-----------------------|--------")
    for book in books:
        status = "Taken" if book[3] else "Available"
        print(f"{book[0]:<4}| {book[1]:<22}| {book[2]:<22}| {status}")


def display_all_members():
    cur.execute("SELECT * FROM Members")
    members = cur.fetchall()

    print("Members:")
    print("ID  | Name")
    print("----|----------------------")
    for member in members:
        print(f"{member[0]:<4}| {member[1]:<22}")


def display_books_taken_by_member(member_id):
    cur.execute(
        """
       SELECT Books.book_id, Books.title, Books.author
       FROM Books
       JOIN Loans ON Books.book_id = Loans.bookid
       WHERE Loans.memberid = {}
    """.format(
            member_id,
        )
    )
    member_books = cur.fetchall()

    if member_books:
        print(f"Books Borrowed by Member {member_id}:")
        print("ID  | Title                 | Author")
        print("----|-----------------------|----------------------")
        for book in member_books:
            print(f"{book[0]:<4}| {book[1]:<22}| {book[2]:<22}")
    else:
        print(f"Member with ID {member_id} not found in books borrowed list")


def display_all_taken_books():
    cur.execute(
        """
         SELECT Books.book_id, books.title, books.author, Members.name, issue_date, due_date
         FROM Books
         JOIN Loans ON Books.book_id = Loans.bookid
         JOIN Members ON Loans.memberid = Members.member_id
     """
    )
    loans = cur.fetchall()

    if loans:
        print("Books Currently Borrowed:")
        print(
            "ID  | Title                 | Author                | Member Name           | Issue Date         | Due Date"
        )
        print(
            "----|-----------------------|-----------------------|-----------------------|--------------------|----------------------"
        )
        for loan in loans:
            print(
                f"{loan[0]:<4}| {loan[1]:<22}| {loan[2]:<22}| {loan[3]:<22}| {loan[4]}| {loan[5]}"
            )
    else:
        print("No books are currently taken.")


def update_loan_status(book_id, member_id):
    # Printing all books

    cur.execute(
        "SELECT * FROM Books WHERE book_id = {} AND availability_status is null".format(
            book_id,
        )
    )
    book = cur.fetchone()
    # Check if the book is available
    if book:
        # Book is available, proceed with loan creation
        cur.execute(
            "INSERT INTO Loans (bookid, memberid) VALUES ({}, {})".format(
                book_id, member_id
            )
        )
        cur.execute(
            "UPDATE Books SET availability_status= 1 WHERE book_id = {}".format(
                book_id,
            )
        )
        cur.execute(
            "UPDATE loans SET due_date = DATE_ADD(NOW(), INTERVAL 14 DAY) where bookid={}".format(
                book_id
            )
        )

        con.commit()
        print(
            f"Book '{book[1]}' taken by Member {member_id}. Due date: {datetime.now() + timedelta(days=14)}"
        )
    else:
        print(f"Book with ID {book_id} is already borrowed or not found.")


def is_member_exists(member_id):
    cur.execute(
        "SELECT * FROM Members WHERE member_id = {}".format(
            member_id,
        )
    )
    return bool(cur.fetchall())


def return_book(member_id, book_id):
    # Check if the book is currently on loan to the specified member

    cur.execute(
        "SELECT * FROM Loans WHERE memberid = {} AND bookid = {}".format(
            member_id, book_id
        )
    )
    loan = cur.fetchone()

    if loan:
        # Book is on loan, proceed with return
        cur.execute(
            "UPDATE Books SET availability_status = null WHERE book_id = {}".format(
                book_id,
            )
        )
        cur.execute(
            "DELETE FROM Loans WHERE id = {}".format(
                loan[0],
            )
        )
        con.commit()
        print(f"Book returned by Member {member_id}.")
    else:
        print(f"Member {member_id} did not borrow the book with ID {book_id}.")


def add_new_member():
    name = input("Enter the name of the new member: ")
    cur.execute(
        "INSERT INTO Members (name) VALUES ('{}')".format(
            name,
        )
    )
    con.commit()
    print(f"New member '{name}' added.")


def add_new_book():
    title = input("Enter the title of the new book: ")
    author = input("Enter the author of the new book: ")
    cur.execute(
        "INSERT INTO Books (title, author) VALUES ('{}', '{}')".format(title, author)
    )
    con.commit()
    print(f"New book '{title}' by {author} added.")


def delete_member():
    memberid = int(input("Enter member ID to be deleted:"))
    if is_member_exists:
        cur.execute(
            "DELETE FROM Members WHERE member_id = {}".format(
                memberid,
            )
        )
        con.commit()
        print(f"Member with ID ", memberid, " has been deleted.")


def main_menu():
    while True:
        print(" \nWelcome to Main Menu")
        print("1. Admin Menu")
        print("2. Member Menu")
        print("3. Exit")

        choice = int(input("Input: "))

        if choice == 1:
            admin_menu()
        elif choice == 2:
            member_menu()
        elif choice == 3:
            break
        else:
            print("Enter a vaild option")


def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. View all books")
        print("2. View all members")
        print("3. View all taken books")
        print("4. Add new Books")
        print("5. Add new member")
        print("6. Delete member")
        print("7. Exit")
        choice = int(input("Input: "))

        if choice == 1:
            display_all_books()
        elif choice == 2:
            display_all_members()
        elif choice == 3:
            display_all_taken_books()
        elif choice == 4:
            add_new_book()
        elif choice == 5:
            add_new_member()
        elif choice == 6:
            delete_member()
        elif choice == 7:
            break
        else:
            print("Enter a vaild choice")


def member_menu():
    member_id = int(input("Enter your member id: "))
    if is_member_exists(member_id):
        while True:
            print("\nMember Menu")
            print("1. View your taken books")
            print("2. Take a new book")
            print("3. Return a taken book")
            print("4. Exit")
            choice = int(input("Input: "))
            if choice == 1:
                display_books_taken_by_member(member_id)
            elif choice == 2:
                display_all_books()
                book_id = int(input("Enter the book id: "))
                update_loan_status(book_id, member_id)
            elif choice == 3:
                book_id = int(input("Enter the book id: "))
                return_book(member_id, book_id)
            elif choice == 4:
                break
            else:
                print("Enter a vaild choice")
    else:
        print("Invalid member id")


if __name__ == "__main__":
    main_menu()
