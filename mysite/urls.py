"""mysite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import url, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django.contrib.sitemaps.views import sitemap
#from sitemaps import PostSitemap


#sitemaps = {
#    "posts": PostSitemap,
#}

admin.site_header = 'The Admin Site'
admin.site.site_title = 'The Admin Site'
admin.site.index_title = 'The Administration'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls"), name="blog-urls"),
    path("summernote/", include("django_summernote.urls")),
#    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
   # path(r'^health/?', include('health_check.urls'))
]


