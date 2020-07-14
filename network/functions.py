from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator
from .models import User, Posts, Likes, Following
import time

# A function to verify if a user liked a particular post
def liked(request, likes):
    for like in likes:
        if like.user.id == request.user.id:
            return True
        else:
            pass
    return False

#A function to verify if a user follows another user
def follows(request, following):
    for follow in following:
        if request.user.id == follow.follower.id:
            return True
        else:
            pass
    return False

#A function for retrieving all post related information
def posts_data(request, posts, right):
    if right:
        result = []
        for post in posts:
            data = {}
            data['id'] = post.id #we will find use for this when editing
            data['user'] = post.user
            data['content'] = post.content
            date = post.time
            data['time'] = time.ctime(date)
            #get the post's likes
            try:
                likes = Likes.objects.filter(post=post).all()
            except Likes.DoesNotExist:
                likes = []
            #see if the current user liked
            liked_post = liked(request, likes)
            #include the likes and who liked in the dictionary
            data['liked'] = liked_post
            data['likes'] = len(likes)
            if post.user.id == request.user.id:
                data['user_post'] = True
            else:
                data['user_post'] = False
            result.append(data)
        
        #the code for page pagination
        paginator = Paginator(result, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return page_obj
    else:
        try:
            user = User.objects.get(pk=request.user.id)
            followed_users = user.follows.all()
        except User.DoesNotExist:
            raise Http404('User does not exist')
        except Posts.DoesNotExist:
            raise Http404('posts does not exist')
        
        followed_list = []
        for followed in followed_users:
            followed_list.append(followed.user)
        
        following = []
        for post in posts:
            if post.user in followed_list:
                following.append(post)
        
        return posts_data(request, following, True)

