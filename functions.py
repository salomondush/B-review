##might need to import other functions that support the database
import os
import requests

from flask import g, request, url_for, redirect, session
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://brqwbfgosrbpmq:ade6836e77834cac05b89bf7c9a05e8be14d7c7e0cc48927cb9f5eafab259a7c@ec2-34-230-149-169.compute-1.amazonaws.com:5432/d1dui1m6484djp")
db = scoped_session(sessionmaker(bind=engine))

#search function  
def book_finder(search):
    search1 = "%" + str(search) + "%"
    
    #first search in authors
    book =  db.execute("SELECT * FROM books WHERE (author LIKE :search) OR (title LIKE :search) OR (CAST(isbn AS TEXT) LIKE :search)", {"search": search1}).fetchall()
    if book:
        return book
    else:
        pass  
    return None

#goodreads api data function
def book_ratings(isbn): 

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "kxJfu32B500v329avf4ZVg", "isbns": isbn})
    if res.status_code != 200:
        return None
    else:
        data = res.json()
        averate_rating = data["books"][0]["average_rating"]
        ratings_count = data["books"][0]["work_ratings_count"]
        return (averate_rating, ratings_count)

#login required function
def login_required(f):
   
    #Decorate routes to require login.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function