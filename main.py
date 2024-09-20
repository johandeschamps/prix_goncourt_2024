from database import session
from models import Author, Book, Selection, Jury, Vote, Publisher

def display_books_by_selection(selection_type):
    """
    Affiche les livres en fonction du type de sélection.

    Args:
        selection_type (str): Le type de sélection des livres à afficher.

    Returns:
        None
    """
    try:
        books = session.query(Book).join(Selection, Book.id == Selection.id).filter(Selection.type == selection_type).all()
        if books:
            for book in books:
                author = session.query(Author).filter(Author.id == book.author_id).first()
                publisher = session.query(Publisher).filter(Publisher.id == book.publisher_id).first()
                print(f"Title: {book.title}\nSummary: {book.summary}\nAuthor: {author.name if author else 'Author not found'}\nPublisher: {publisher.name if publisher else 'Publisher not found'}\nPublication Date: {book.publication_date}\nPages: {book.pages}\nISBN: {book.isbn}\nPublisher Price: {book.publisher_price}\n")
        else:
            print(f"No books found for the selection {selection_type}.")
    except Exception as e:
        print(f"Error displaying books: {e}")

def add_book_to_selection(book_id, selection_type):
    """
    Ajoute un livre à une sélection.

    Args:
        book_id (int): L'ID du livre à ajouter.
        selection_type (str): Le type de sélection auquel ajouter le livre.

    Returns:
        None
    """
    try:
        if selection_type == 'First':
            date = '2024-09-19'
        elif selection_type == 'Second':
            date = '2024-10-01'
        elif selection_type == 'Third':
            date = '2024-10-22'
        else:
            print(f"Type of selection {selection_type} Not recognized.")
            return

        selection = Selection(date=date, type=selection_type)
        session.add(selection)
        session.commit()
        print(f"Book ID {book_id} added to the selection {selection_type}.")
    except Exception as e:
        print(f"Error adding book to selection: {e}")

def display_votes():
    """
    Affiche tous les votes enregistrés.

    Returns:
        None
    """
    try:
        votes = session.query(Vote).all()
        if votes:
            for vote in votes:
                book = session.query(Book).filter(Book.id == vote.book_id).first()
                print(f"Book: {book.title if book else 'Book not found'}, Votes: {vote.votes}")
        else:
            print("No votes found.")
    except Exception as e:
        print(f"Error displaying votes: {e}")

def authenticate_member(name, role):
    """
    Authentifie un membre du jury.

    Args:
        name (str): Le nom du membre du jury.
        role (str): Le rôle du membre du jury.

    Returns:
        Jury: L'objet membre du jury si authentifié, sinon None.
    """
    try:
        member = session.query(Jury).filter(Jury.name == name, Jury.role == role).first()
        if member:
            print(f"Authentication successful for {name} with role {role}.")
            return member
        else:
            print("Authentication failed.")
            return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def vote(member_id, book_id):
    """
    Enregistre un vote pour un livre par un membre du jury.

    Args:
        member_id (int): L'ID du membre du jury.
        book_id (int): L'ID du livre pour lequel voter.

    Returns:
        None
    """
    try:
        vote = session.query(Vote).filter(Vote.book_id == book_id, Vote.jury_member_id == member_id).first()
        if vote:
            vote.votes += 1
        else:
            vote = Vote(book_id=book_id, jury_member_id=member_id, votes=1)
            session.add(vote)
        session.commit()
        print(f"Vote recorded for book ID {book_id} by member ID {member_id}.")
    except Exception as e:
        print(f"Error recording vote: {e}")

def main_menu():
    """
    Affiche le menu principal et gère les interactions utilisateur.

    Returns:
        None
    """
    while True:
        print("Welcome to the Prix Goncourt 2024")
        print("1. User")
        print("2. Jury Chairman")
        print("3. Jury Member")
        print("4. Quit")
        choice = input("Please select your role (1/2/3/4): ")

        if choice == '1':
            print("You chose: User")
            selection_type = input("Please enter the type of selection to display (First/Second/Third): ")
            display_books_by_selection(selection_type)
        elif choice == '2':
            print("You chose: Jury President")
            name = input("Please enter your name: ")
            role = 'President'  # Using the role 'President'
            member = authenticate_member(name, role)
            if member:
                action = input("What would you like to do? (display_books/add_book/display_votes): ")
                if action == 'display_books':
                    selection_type = input("Please enter the type of selection to display (First/Second/Third): ")
                    display_books_by_selection(selection_type)
                elif action == 'add_book':
                    book_id = int(input("Please enter the ID of the book to add: "))
                    selection_type = input("Please enter the type of selection (First/Second/Third): ")
                    add_book_to_selection(book_id, selection_type)
                elif action == 'display_votes':
                    display_votes()
                else:
                    print("Unrecognized action.")
            else:
                print("Authentication failed.")
        elif choice == '3':
            print("You chose: Jury Member")
            name = input("Please enter your name: ")
            role = 'Member'
            member = authenticate_member(name, role)
            if member:
                book_id = int(input("Please enter the ID of the book you want to vote for: "))
                vote(member.id, book_id)
            else:
                print("Authentication failed.")
        elif choice == '4':
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
