from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


def __str__(self):
    return self.title

STATUS = ((0, "Draft"), (1, "Publish"))


class MainTextt(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    text_field = models.TextField(blank=True, default='')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    readonly_fields = ('created_on', 'updated_on')
    def __str__(self):
        return self.text_field



class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
#    category = models.CharField(max_length=200, default='Uncategorized')
    tags = TaggableManager()
#    common_tags = tags.common_tags()[:2]


    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", kwargs={"slug": str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("home")

