from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html")

@app.route("/inspirations")
def inspirations():
    return render_template("inspirations.html")

