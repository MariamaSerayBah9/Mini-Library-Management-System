# library_system.py
# Simple Library Management System for Beginners

# ---- Step 1: Create basic data storage ----
genres = ("Fiction", "Non-Fiction", "Sci-Fi", "Mystery")

books = {}      # example: {"ISBN1": {"title": "Python 101", "author": "John", "genre": "Fiction", "copies": 2}}
members = []    # example: [{"id": "M001", "name": "Alice", "email": "a@mail.com", "borrowed": []}]

# ---- Step 2: Add a book ----
def add_book(isbn, title, author, genre, copies):
    if isbn in books:
        print("❌ Book already exists!")
        return
    if genre not in genres:
        print("❌ Invalid genre!")
        return
    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "copies": copies
    }
    print("✅ Book added successfully!")

# ---- Step 3: Add a member ----
def add_member(member_id, name, email):
    for m in members:
        if m["id"] == member_id:
            print("❌ Member already exists!")
            return
    members.append({"id": member_id, "name": name, "email": email, "borrowed": []})
    print("✅ Member added successfully!")

# ---- Step 4: Borrow a book ----
def borrow_book(member_id, isbn):
    for m in members:
        if m["id"] == member_id:
            if isbn not in books:
                print("❌ Book not found!")
                return
            book = books[isbn]
            if book["copies"] == 0:
                print("❌ No copies left!")
                return
            if len(m["borrowed"]) >= 3:
                print("❌ Member already borrowed 3 books!")
                return
            m["borrowed"].append(isbn)
            book["copies"] -= 1
            print("✅ Book borrowed successfully!")
            return
    print("❌ Member not found!")

# ---- Step 5: Return a book ----
def return_book(member_id, isbn):
    for m in members:
        if m["id"] == member_id:
            if isbn not in m["borrowed"]:
                print("❌ This book was not borrowed by this member!")
                return
            m["borrowed"].remove(isbn)
            books[isbn]["copies"] += 1
            print("✅ Book returned successfully!")
            return
    print("❌ Member not found!")

# ---- Step 6: Search for a book ----
def search_book(keyword):
    found = False
    for isbn, book in books.items():
        if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower():
            print(f"🔍 Found: {book['title']} by {book['author']} ({book['genre']})")
            found = True
    if not found:
        print("❌ No book found with that keyword.")

# ---- Step 7: Show all books and members ----
def show_data():
    print("\n📚 All Books:")
    for isbn, b in books.items():
        print(f"{isbn} → {b['title']} by {b['author']} | {b['genre']} | Copies: {b['copies']}")
    print("\n👥 All Members:")
    for m in members:
        print(f"{m['id']} → {m['name']} | Borrowed: {m['borrowed']}")

# ---- Step 8: Demo ----
def demo():
    print("\n=== MINI LIBRARY SYSTEM DEMO ===\n")

    add_book("B001", "Python Basics", "John Smith", "Non-Fiction", 2)
    add_book("B002", "Space Mystery", "Jane Doe", "Sci-Fi", 1)

    add_member("M001", "Alice", "alice@mail.com")
    add_member("M002", "Bob", "bob@mail.com")

    borrow_book("M001", "B001")
    borrow_book("M002", "B002")
    borrow_book("M001", "B002")  # should fail (no copies left)

    search_book("Python")

    return_book("M001", "B001")

    show_data()

# Run demo automatically
demo()