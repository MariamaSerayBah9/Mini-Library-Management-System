# operations.py
"""
Mini Library Management System - operations module
Uses:
- books: dict keyed by ISBN -> {title, author, genre, total_copies, available_copies}
- members: list of dicts -> {member_id, name, email, borrowed_books}
- GENRES: tuple of allowed genres
"""

GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Mystery", "Fantasy")

books = {}    # global dict: ISBN -> book dict
members = []  # global list of member dicts

# ---------------------------
# Helper utilities
# ---------------------------
def find_member(member_id):
    for m in members:
        if m["member_id"] == member_id:
            return m
    return None

# ---------------------------
# Book operations
# ---------------------------
def add_book(isbn, title, author, genre, total_copies):
    if isbn in books:
        return False, "ISBN already exists."
    if genre not in GENRES:
        return False, f"Invalid genre. Valid genres: {GENRES}"
    if total_copies <= 0:
        return False, "total_copies must be > 0"
    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": int(total_copies),
        "available_copies": int(total_copies)
    }
    return True, "Book added."

def update_book(isbn, **kwargs):
    if isbn not in books:
        return False, "Book not found."
    book = books[isbn]
    # allow updating title, author, genre, total_copies
    if "genre" in kwargs and kwargs["genre"] not in GENRES:
        return False, "Invalid genre."
    if "total_copies" in kwargs:
        new_total = int(kwargs["total_copies"])
        borrowed = book["total_copies"] - book["available_copies"]
        if new_total < borrowed:
            return False, "Cannot set total_copies less than currently borrowed copies."
        # adjust available_copies accordingly
        book["available_copies"] = new_total - borrowed
        book["total_copies"] = new_total
    for k in ("title", "author", "genre"):
        if k in kwargs:
            book[k] = kwargs[k]
    return True, "Book updated."

def delete_book(isbn):
    if isbn not in books:
        return False, "Book not found."
    book = books[isbn]
    borrowed = book["total_copies"] - book["available_copies"]
    if borrowed > 0:
        return False, "Cannot delete: some copies are borrowed."
    del books[isbn]
    return True, "Book deleted."

def search_books(query, field="title"):
    """
    Search by 'title' or 'author' (case-insensitive, substring).
    Returns list of (isbn, book_dict)
    """
    q = query.lower()
    results = []
    for isbn, b in books.items():
        if field == "title" and q in b["title"].lower():
            results.append((isbn, b.copy()))
        elif field == "author" and q in b["author"].lower():
            results.append((isbn, b.copy()))
    return results

# ---------------------------
# Member operations
# ---------------------------
def add_member(member_id, name, email):
    if find_member(member_id) is not None:
        return False, "Member ID already exists."
    members.append({
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []  # list of ISBNs
    })
    return True, "Member added."

def update_member(member_id, **kwargs):
    m = find_member(member_id)
    if not m:
        return False, "Member not found."
    for k in ("name", "email"):
        if k in kwargs:
            m[k] = kwargs[k]
    return True, "Member updated."

def delete_member(member_id):
    m = find_member(member_id)
    if not m:
        return False, "Member not found."
    if len(m["borrowed_books"]) > 0:
        return False, "Cannot delete member: they have borrowed books."
    members.remove(m)
    return True, "Member deleted."

# ---------------------------
# Borrow / Return
# ---------------------------
def borrow_book(member_id, isbn):
    m = find_member(member_id)
    if not m:
        return False, "Member not found."
    if isbn not in books:
        return False, "Book not found."
    book = books[isbn]
    if book["available_copies"] <= 0:
        return False, "No copies available."
    if len(m["borrowed_books"]) >= 3:
        return False, "Member reached borrow limit (3)."
    # Borrow
    m["borrowed_books"].append(isbn)
    book["available_copies"] -= 1
    return True, "Book borrowed."

def return_book(member_id, isbn):
    m = find_member(member_id)
    if not m:
        return False, "Member not found."
    if isbn not in m["borrowed_books"]:
        return False, "This book is not recorded as borrowed by member."
    m["borrowed_books"].remove(isbn)
    if isbn in books:
        books[isbn]["available_copies"] += 1
    return True, "Book returned."

# ---------------------------
# Utility (for demo)
# ---------------------------
def list_books():
    return {isbn: b.copy() for isbn, b in books.items()}

def list_members():
    return [m.copy() for m in members]