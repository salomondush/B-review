import os
import requests

from flask import g, request, url_for, redirect, session
from functools import wraps

#login required function
def login_required(f):
   
    #Decorate routes to require login.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function