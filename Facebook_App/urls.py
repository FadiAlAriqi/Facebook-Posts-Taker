from django.urls import path
from . import views
# from views import home, fetch_posts, search
# from Facebook_App.views import home, fetch_posts, search

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch_posts', views.fetch_posts, name='fetch_posts'),
    path('search', views.search, name='search'),
    path('search0', views.search0, name='search0'),
    path('posts', views.posts, name='posts'),
    path('posts/view/<str:post_id>/', views.view_post, name='view_post')
]