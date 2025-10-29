from operations import (
    books, members,
    add_book, add_member, borrow_book, return_book, delete_book, delete_member
)


def run_tests():
    """Run all tests for the library system"""

    # Clear previous data before starting tests
    books.clear()
    members.clear()

    print("Running Library Management System Tests...")
    print("=" * 50)

    # Test 1: Add a book successfully
    print("Test 1: Adding a new book...")
    success, message = add_book("ISBN1", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1)
    assert success, f"FAILED: {message}"
    print("PASSED: Book added successfully")

    # Test 2: Prevent adding duplicate ISBN
    print("\nTest 2: Preventing duplicate ISBN...")
    success, message = add_book("ISBN1", "Different Title", "Different Author", "Fiction", 1)
    assert not success, "FAILED: Should not allow duplicate ISBN"
    print("PASSED: Duplicate ISBN correctly rejected")

    # Test 3: Add member and test borrowing
    print("\nTest 3: Adding member and borrowing book...")
    success, message = add_member("U1", "John Doe", "john@example.com")
    assert success, f"FAILED: {message}"
    print("PASSED: Member added successfully")

    # First borrow should succeed
    success, message = borrow_book("U1", "ISBN1")
    assert success, f"FAILED: {message}"
    print("PASSED: First borrow successful")

    # Second borrow should fail (no copies left)
    success, message = borrow_book("U1", "ISBN1")
    assert not success, "FAILED: Should not allow borrowing when no copies available"
    print("PASSED: Second borrow correctly rejected (no copies available)")

    # Test 4: Returning a book
    print("\nTest 4: Returning a borrowed book...")
    success, message = return_book("U1", "ISBN1")
    assert success, f"FAILED: {message}"
    print("PASSED: Book returned successfully")

    # Should be able to borrow again after return
    success, message = borrow_book("U1", "ISBN1")
    assert success, f"FAILED: {message}"
    print("PASSED: Can borrow again after return")

    # Test 5: Prevent deleting borrowed book
    print("\nTest 5: Preventing deletion of borrowed book...")
    success, message = delete_book("ISBN1")
    assert not success, "FAILED: Should not allow deleting borrowed book"
    print("PASSED: Cannot delete borrowed book")

    # Test 6: Prevent deleting member with borrowed books
    print("\nTest 6: Preventing deletion of member with borrowed books...")
    success, message = delete_member("U1")
    assert not success, "FAILED: Should not allow deleting member with borrowed books"
    print("PASSED: Cannot delete member with borrowed books")

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED! 🎉")


# Run the tests
if __name__ == "__main__":
    run_tests()