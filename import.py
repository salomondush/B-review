import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#use this (URI, pool_recycle=3600) if the connection timeout persists with a good internet connection 
engine = create_engine("postgres://brqwbfgosrbpmq:ade6836e77834cac05b89bf7c9a05e8be14d7c7e0cc48927cb9f5eafab259a7c@ec2-34-230-149-169.compute-1.amazonaws.com:5432/d1dui1m6484djp")
db = scoped_session(sessionmaker(bind=engine))


#insert information from books.csv into the database
def main():
    f = open("books.csv")
    reader = csv.reader(f)
    #bcs the csv contains a header as first row. Now, we must skip it 
    next(reader, None)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
        {"isbn": isbn, "title": title, "author": author, "year": year})
        
        db.commit()

if __name__ == "__main__":
    main()
