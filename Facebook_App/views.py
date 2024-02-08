from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Post
from django.db.models import Sum
from django.db.models import Count
import requests

access_token = ''

def home(request):
    return render(request, 'index.html')

def get_likes_count(post_id, access_token):
    api_url = f"https://graph.facebook.com/{post_id}/likes?summary=true&access_token={access_token}"
    response = requests.get(api_url)
    data = response.json()
    likes_count = data['summary']['total_count']
    return likes_count

def get_comments_count(post_id, access_token):
    api_url = f"https://graph.facebook.com/{post_id}/comments?access_token={access_token}"
    response = requests.get(api_url)
    data = response.json()
    comments_count = len(data.get('data', []))
    return comments_count

def get_shares_count(post_id, access_token):
    api_url = f"https://graph.facebook.com/{post_id}/sharedposts?access_token={access_token}"
    response = requests.get(api_url)
    data = response.json()
    shares_count = len(data.get('data', []))
    return shares_count


def view_post(request, post_id):
    post = Post.objects.get(post_id=post_id) 
    return redirect(post.url)


def fetch_posts(request):
    global access_token
    if request.method == 'POST':
        page_id = request.POST['page_id']
        num_posts = int(request.POST['num_posts'])
        access_token = request.POST['access_token']

        # Delete Posts from Database
        Post.objects.all().delete()

        # API to get posts from my page in facebook
        api_url = f"https://graph.facebook.com/{page_id}/posts?access_token={access_token}&limit={num_posts}"
        response = requests.get(api_url)
        data = response.json()

        # Save data in database
        for post_data in data['data']:
            post_id = post_data['id']
            message = post_data['message'] if 'message' in post_data else ''
            likes = get_likes_count(post_id, access_token)
            comments = get_comments_count(post_id, access_token)
            shares = get_shares_count(post_id, access_token)
            url = f"https://www.facebook.com/{page_id}/posts/{post_id}"

            post = Post(post_id=post_id, message=message, likes=likes, comments=comments, shares=shares, url=url)
            post.save()

        # Update shares count in the database
        update_shares_count()

        # View the posts stored in the database
        return posts(request)
    else:
        return HttpResponse('Method Not Allowed')


def update_shares_count():
    posts = Post.objects.all()
    for post in posts:
        shares_count = get_shares_count(post.post_id, access_token)
        post.shares = shares_count
        post.save()


def posts(request):
    posts = Post.objects.annotate(shares_count=Count('shares'))
    total_likes = Post.objects.aggregate(total_likes=Sum('likes'))['total_likes']
    total_comments = Post.objects.aggregate(total_comments=Sum('comments'))['total_comments']
    total_shares = Post.objects.aggregate(total_shares=Sum('shares'))['total_shares']

    return render(request, 'posts.html', {'posts': posts, 'total_likes': total_likes, 'total_comments': total_comments, 'total_shares': total_shares})

def search0(request):
    return render(request, 'search.html')


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        results = Post.objects.filter(message__icontains=keyword)
        return render(request, 'search.html', {'results': results})
    else:
        return HttpResponse('Method Not Allowed')