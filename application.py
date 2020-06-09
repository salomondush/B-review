import os

from flask import Flask, session, redirect, render_template, request, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
#import the functions python file
from functions import * 


app = Flask(__name__)

#templates to be auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Check for environment variable
if not "DATABASE_URL":
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
engine = create_engine("postgres://brqwbfgosrbpmq:ade6836e77834cac05b89bf7c9a05e8be14d7c7e0cc48927cb9f5eafab259a7c@ec2-34-230-149-169.compute-1.amazonaws.com:5432/d1dui1m6484djp")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        #get information of any 10 books in the database of books
        books = db.execute("SELECT * FROM books LIMIT 10").fetchall()
        return render_template("home.html", books = books)
    else:
        #get the title, isbn, or author.
        search = request.form.get('search')
        
        #call the finder function
        books = book_finder(search)

        #if not book is found
        if books == None:
            return render_template("searched.html", error = "No book found")
        else:
            #return the search results 
            return render_template('searched.html', books = books)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        #check if user email exists
        rows = db.execute("SELECT * FROM users WHERE email = :email", {'email': email}).fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], password):
            return render_template('login.html', error = "Cannot find user, Email or Password incorrect!") #find a place for this word in login.html
        else:
            #log user in
            #set session for user
            session['user_id'] = rows[0]['id']

            #reditect to homepage
            return redirect('/')

@app.route("/register", methods = ["GET", "POST"])
def register():
    #register user
    if request.method == "POST":
        #get email and password
        email = request.form.get('email')
        p_hash = generate_password_hash(request.form.get('pass1'))

        #check if user with email doesn't exist already
        user = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchall()
        if user:
            return render_template("register.html", user_error = "User with email already exists")
        else:
            #insert user into the database
            id = db.execute("INSERT INTO users (email, hash) VALUES (:email, :hash) RETURNING id", {"email": email, "hash": p_hash})
            db.commit()

            #get lastrowid
            for number in id:
                lastId = number[0]

            #set session for new user
            session["user_id"] = lastId

            #redirect to homepage
            return redirect('/')
    else:
        return render_template("register.html")

@app.route('/book/<int:book_id>', methods = ["GET", "POST"])
@login_required
def book(book_id):
    """Lists details about a single book."""
    if request.method == "GET":

        #Store the book id to be used later
        session["book_id"] = book_id

        #no user can submit ratings for the same book two times (not right)
        user = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": session['user_id'], "book_id": book_id}).fetchone()
        
        #get book details from the databse
        book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()

        #get the GoodReads ratings
        book_isbn = book[1] 
        ratings = book_ratings(book_isbn)

        #get all of the other user's ratings and reviews on this book
        user_reviews = db.execute("SELECT * FROM reviews WHERE book_id = :id", {"id": book_id}).fetchall()
        
        #get all of this information to the user
        return render_template("book.html", book = book, ratings = ratings, user_reviews = user_reviews, user = user)


@app.route("/api/<isbn>")
def books_api(isbn):

    #get book from the database
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"Error": "Invalid book isbn"}), 404 #status code (not found on server)
    else:
        #get the book review details
        book_id = book[0]
        book_review_count = db.execute("SELECT COUNT(*) FROM reviews WHERE book_id = :book_id", {"book_id": book_id})

        #assign variables
        title = book[2]
        author = book[3]
        year = book[4]
        count = [dict(number) for number in book_review_count]
        
        #get book ratings (the fetchall function returns a list of elements or an empty list,
        #WHILE the fetchone() function returns None or an elemet. Also you can combine two SQL queries
        #with OR, AND)
        book_ratings = db.execute("SELECT rating FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchall()
        if book_ratings == []:
            return jsonify({
            "title": title,
            "author": author,
            "year": year,
            "review_count": count[0]['count'],
            "average_score": "no ratings yet"
            })
            
        else:
            count = 0
            for rating in book_ratings:
                count += int(rating[0])
            #include an error handling code to captuer exceptions
            try:
                average_rating = (count/ len(book_ratings))
            except ZeroDivisionError:
                pass
            
            return jsonify({
            "title": title,
            "author": author,
            "year": year,
            "review_count": count,
            "average_score": average_rating
            })

#the function to submit user ratings to the database
@app.route("/ratings", methods = ["POST"])
@login_required
def ratings():
    #get the user's review
    number = request.form.get('number')
    review = request.form.get('review')

    #insert the review into the database
    db.execute("INSERT INTO reviews (user_id, rating, review, book_id) VALUES (:user_id, :rating, :review, :book_id)", {"user_id": session["user_id"], "rating": number, "review": review, "book_id": session["book_id"]})
    db.commit()
        
    #redirect home
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    #log user out by clearing sessions 

    session.clear()

    #redirect user
    return redirect('/')