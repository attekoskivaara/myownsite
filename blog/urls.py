from . import views
from django.urls import include, path
from .feeds import LatestPostsFeed, AtomSiteNewsFeed
from .dash_apps import co_by_sector
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect



urlpatterns = [
    #path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("blog/", views.PostList.as_view(), name="blog"),
    path('', views.PostList.as_view(), name='home'),
    path('tag/<slug:tag_slug>', views.TagIndexView.as_view(), name='posts_by_tag'),
    path("contact", views.contact, name="contact"),
    path("co2", views.co2, name="co2"),
 #   path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('geartracker/', include('gear_app.urls')),
    path('activities/', include('activities_app.urls')),
    path('user/', include('user_app.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='user_app/login.html'), name='login'),
    path('user_app/', include('user_app.urls')),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
   # path('user/', views.dashboard_view, name='user'),
 #   path('', lambda request: redirect('user')),  # Root -> dashboard

]

