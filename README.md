# Project 1

Web Programming with Python and JavaScript

B reviews

        This is a book review website, B reviews. It is a book review webiste where users come and leave ratings and reviews on any book they want.
        
        An external source included to get book ratings is Goodreads book_reviews API, which returns back a JSON containing all rating information about a particular book. Another extenal source is Heroku, which is the location of our database.

TEMPLATES(pages).

NB: The user is only able to view the navigation bar, login and register pages when not logged in. Other pages are acccessed only when logged in.

    - Login: This page allows users to login inorder to access or record book reviews using an email and the account's password. It checks if the user actually exists before logging in. 

    - register: New users are able to create new acounts on this page with only an email address and a password. This page checks if passwords match or if the user doesn't already exist inorder to allow you to register. 

    - home.html: This page includes a search area that allows users to search for books in our heroku database. A user can search using part/full ISBN, Author's name, or Book's title. Also, it displays a sample of the books in our databse in a table format. 

    - searched.html: After a search is made in the home.html, the page directs the user to this page where a list of search description matching books are presented. Here, the user is able to click on any book in their results to get generel book information and its Goodreads reviews and ratings. More important, the user can view and submit ratings.

    - book.html: When a book is selected from the search results in searched.html, he/she is directed to this page, where general book informtion, like author, title, release year, and goodreads ratings, is displayed. Moreovere, the user is able to see other user's ratings on the book, and is also able to submit his/her rating and review. One user cannot review the same book two times; the submit button gets immidiately disabled. 

    -logout: The user can logout at any time from where the current session is cleared. 

PYTHON FILES:
    
    - application.py: This file includes the whole python code running on our server to make all of the above actions possible

    - functions.py: This python file includes the search, API, and the login_required functions. The login required function allows as to make some pages unavailable when the user tries to get them without logging in first. 

    - import.py: All of the books in our database are imported from a csv file of 5000 books using the code in this python file. 

DATABASE(TABLES):

    - users table: This table corrects all users' credentials: email and hashed password. It has columns id, email, and hash.

    - books table: All of the books and related information are stored in this table. id, isbn, title, author, and year are all columns of data in this table. 

    - reviews table: with user_id, rating, review, and book_id columns, this table stores all data related to reviews and ratings. This data is connected to a certain book and user using user and book ids as foreign keys. 

REQUIREMENTS: the requirement text file includes all of the required modules to run this project. 


