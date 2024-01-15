from . import views
from django.urls import include, path
from .feeds import LatestPostsFeed, AtomSiteNewsFeed
from .dash_apps import co_by_sector


urlpatterns = [
    path("", views.home, name="home"),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("blog/", views.PostList.as_view(), name="blog"),
    # re_path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path('tag/<slug:tag_slug>', views.TagIndexView.as_view(), name='posts_by_tag'),
    path("contact", views.contact, name="contact"),
    path("co2", views.co2, name="co2"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

]

