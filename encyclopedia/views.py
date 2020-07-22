from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from . import util

import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": False
    })

def title(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {"error": "Page Not Found!"}) 
    else:
        return render(request, "encyclopedia/title.html", {"entry": markdown2.markdown(entry), "title": title})

def search(request):
    title = request.POST["title"]
    entries = util.list_entries()
    
    #now let's look for matches
    match = []
    if title in entries:
        return HttpResponseRedirect(reverse("title", args=(title,)))
    else:
        for entry in entries:
            if title in entry:
                match.append(entry)

    #now we should render this to the index page
    return render(request, "encyclopedia/index.html", {"entries": match, "search": True})

def newentry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newentry.html")
    else:
        title = request.POST.get("title")
        content = request.POST.get("content")
        #check if not exists already
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/error.html", {"error": "Entry Already Exists!"})
        else:
            #save the new entry
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=(title,)))

def edit(request, entry_title):
    if request.method == "GET":
        entry = util.get_entry(entry_title)
        return render(request, "encyclopedia/edit.html", {"content": entry, "title": entry_title})
    else:
        content = request.POST.get("content")
        #save the users entry
        util.save_entry(entry_title, content)
        #redirect to the entries page
        return HttpResponseRedirect(reverse("title", args=(entry_title,)))
    
    
def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("title", args=(entry,)))