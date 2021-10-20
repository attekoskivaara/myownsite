from . import views
from django.urls import include

from django.urls import path
from .feeds import LatestPostsFeed, AtomSiteNewsFeed
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("blog/", views.PostList.as_view(), name="blog"),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path('tag/<slug:tag_slug>', views.TagIndexView.as_view(), name='posts_by_tag'),
    path("contact", views.contact, name="contact"),
    path("", views.home, name="home")
]

