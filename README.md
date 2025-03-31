# 📚 Library Management System

## 📖 Overview
The **Library Management System** is a software application designed to facilitate the efficient management of a library.
It provides functionalities for both administrators and members, allowing them to perform tasks such as adding books, managing members, checking out books, and viewing borrowed history.

##  Features

### 🔑 Login Module
- Users must select their role as either **ADMIN** or **USER**.
- **Admin** has full control over the library system, including managing books and members.
- **User** can log in using their **Member ID** and access library services accordingly.

###  Admin Menu
1. **📚 Add Book**  
   *Function:* `add_new_book()`  
   - Allows administrators to add new books by entering details such as **title** and **author**.

2. **📖 View All Books**  
   *Function:* `display_all_books()`  
   - Displays a **comprehensive list** of all books available in the library.
     
3. **👥 Manage Members**  
   *Functions:* `add_new_member()`, `delete_member()`  
   - Enables administrators to **add** new members and **remove** existing members from the system.

4. **👤 View All Members**  
   *Function:* `display_all_members()`  
   - Displays a list of all registered **library members**.

5. **📊 Generate Reports**  
   *Function:* `display_all_taken_books()`  
   - Allows admins to generate reports on **book availability** and **member activities**.

### 📌 Member Menu
1. **🔍 Search for Books**  
   *Function:* `display_all_books()`  
   - Members can search for books based on **title, author**, or other criteria.

2. **📥 Check Out Books**  
   *Function:* `update_loan_status()`  
   - Members can borrow books, updating the system accordingly.

3. **📤 Return Books**  
   *Function:* `return_book()`  
   - Members can return borrowed books, updating the **library database**.

4. **📜 View Borrowed History**  
   *Function:* `display_books_taken_by_member()`  
   - Members can check their **borrowing history**, including **book titles, authors, issue dates, and return dates**.



---

## 🎯 Usage
- **Admins** should log in with administrative credentials to **manage books and members**.
- **Members** can log in using their **Member ID** to **search, borrow, and return books**.

---

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).

---

## 🤝 Contributions
Contributions are welcome! Feel free to **fork the repository**, create **feature branches**, and submit **pull requests**.

---

Jerusha

