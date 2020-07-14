from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts, Likes, Following
from .functions import liked, posts_data, follows

import time

def index(request):
    try:
        posts = Posts.objects.order_by("-time").all()
    except Posts.DoesNotExist:
        raise Http404("posts does not exist")
    #get all post related data
    page_obj = posts_data(request, posts, True)

    return render(request, "network/index.html", {"page_obj": page_obj})

def following(request):
    try:
        posts = Posts.objects.order_by("-time").all()
    except Posts.DoesNotExist:
        raise Http404('posts does not exist')

    page_obj = posts_data(request, posts, False)

    return render(request, "network/index.html", {"page_obj": page_obj})

def profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_posts = user.posts.order_by("-time")
        followers = user.followers.all()
        following = user.follows.all()
    except User.DoesNotExist:
        raise Http404("User does not exist")
    except User.AttributeError:
        raise Http404("Posts or followers or following does not exist")
    
    #check if you follow user
    following_user = follows(request, followers)
    #get posts data
    page_obj = posts_data(request, user_posts, True)

    #make sure a user can't follow him/her self.
    if user.id == request.user.id:
        follow = False
    else:
        follow = True

    context = {
        "posts_number": len(user_posts),
        "followers_number": len(followers),
        "following_number": len(following),
        "user_name": user.username,
        "page_obj": page_obj,
        "follows": following_user,
        "id": user.id,
        "follow": follow
    }

    return render(request, 'network/profile.html', context)

def edit_post(request): ######
    new_content = request.GET.get('content')
    post_id = int(request.GET.get('post_id'))
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        raise Http404("Post doesn't exist!")
    #update the posts content.
    post.content = new_content
    post.save()

    #retrieve new info after update
    try: 
        post = Posts.objects.get(pk=post_id)
        username = post.user.username
        user_id = post.user.id
        likes = post.likes.count()
        date = time.ctime(post.time)
    except Posts.DoesNotExist:
        raise Http404('post does not exist')

    return JsonResponse({
        "user_id": user_id,
        "username": username,
        "content": new_content,
        "time": date,
        "likes": likes
    })


def new_post(request):
    #get the needed data
    post_content = request.GET.get('content')
    date = time.time()
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        raise Http404("user doesn't exist")
    #create a new post instance
    Posts.objects.create(user=user, content=post_content, time=date)

    #retrieve new post info
    try: 
        post_id = Posts.objects.latest('id').id
    except Posts.DoesNotExist:
        raise Http404("Post does not exist")


    return JsonResponse({
        "id": post_id,
        "content": post_content,
        "username": user.username,
        "user_id": user.id,
        "date": time.ctime(date),
        "liked": False
    })

def like(request):
    #get the post's like
    like = int(request.GET.get('like') or 0)
    id = int(request.GET.get('id'))
    #get post likes
    try:
        post = Posts.objects.get(pk=id)
    except Posts.DoesNotExist:
        raise Http404('Post does not exist!')

    #insert or remove
    if like > 0:
        Likes.objects.create(user=request.user, post=post)
    else:
        Likes.objects.filter(user=request.user, post=post).delete()

    #Now get the new total number of likes for a post
    return JsonResponse({
        "likes": post.likes.count()
    })

def follow(request):
    #get the new follower and the user being followed
    follower = int(request.GET.get('follow') or 0)
    id = int(request.GET.get('id'))

    #get the user whose id is id
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        raise Http404('User does not exist')

    #if a follow or unfollow
    if follower > 0:
        Following.objects.create(user=user, follower=request.user)
    else:
        Following.objects.filter(user=user, follower=request.user).delete()


    return JsonResponse({
        "followers": user.followers.count()
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
