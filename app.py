from models import (Book, engine, session, Base)
import datetime
import csv

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def menu():
    while True:
        print("""
        \rPROGRAMMING BOOKS
        \r1) Add book
        \r2) View all books
        \r3) Search for a book
        \r4) Book Analysis
        \r5) Exit
        """)
        choice = input("What would you like to do? ")
        if choice in ['1','2','3','4','5']:
            return choice
        else:
            print("Please choose one of [1, 2, 3, 4, 5]")

def add_book():
    print("\rAdd a New Book")
    title = input("Book title: ")
    author = input("Author: ")
    published = input("Published (Example: January 13, 2003): ")
    price = input("Price (Example: 10.99): ")

    new_book = create_book([title, author, published, price])
    session.add(new_book)
    session.commit()
    print("Book added!")

def create_book(book):
    """ 
    @param: book is a list of book descriptions of a book
    @return Book object
    """
    title = book[0]
    author = book[1]
    published = book[2]
    price = book[3]

    published_date = datetime.datetime.strptime(published, "%B %d, %Y")
    price = int(float(price) * 100)
    return Book(title=title, author=author, published_date=published_date, price=price)

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                session.add(create_book(row))
    session.commit()

def view_books():
    books = session.query(Book).all()
    for book in books:
        display_book(book)
        pause()

def search_book():
    ids = [book.id for book  in session.query(Book.id)]
    print(f"Options: {ids}")
    id = int(input("What is the book's id? "))
    book = session.query(Book).filter_by(id=2).one()
    display_book(book)

def analyze_books():
    newest_book = session.query(Book).order_by(Book.published_date).first()
    oldest_book = session.query(Book).order_by(Book.published_date.desc()).first()
    total = session.query(Book).count()
    total_python = session.query(Book).filter(Book.title.like("%Python%")).count()
    print(f"Newest book: {newest_book}")
    print(f"Oldest book: {oldest_book}")
    print(f"Total number of books: {total}")
    print(f"Total number of Python books: {total_python}")
    pause()

def display_book(book):
    print(f"""
    \r{book.title} by {book.author}
    \rPublished: {book.published_date.strftime('%B %d, %Y')}
    \rPrice: ${float(book.price)/100:.2f}
    """)

def pause():
    input("Press the <ENTER> key to continue...")

def app():
    app_running = True
    while(app_running):
        choice = menu()
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            analyze_books()
        else:
            print("Goodbye")
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
    # add_csv()

