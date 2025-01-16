from django.urls import path
from . import views

"""
This module contains the URL routing for the 'blog' application in the Django
project.

It defines the URL patterns for various views in the blog section of the
website, mapping HTTP requests to the corresponding view functions or
class-based views.

URL patterns:
    - The root URL (''): Maps to the StartingPageView to show recent blog
      posts.
    - '/posts': Maps to the PostsView to display a list of all blog posts.
    - '/posts/<slug:slug>': Maps to the PostDetailView to display a single
      post's details.
    - '/read-later': Maps to the ReadLaterView to show posts saved for later
      reading.

Each URL pattern also defines a named URL, which can be used for reverse URL
resolution in templates and views.
"""


urlpatterns = [
    path('', views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.PostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.PostDetailView.as_view(),
         name='post-detail-page'),
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]
