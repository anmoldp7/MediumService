from django.db import models
from django.utils import timezone

class BlogTag(models.Model):
    tag_name = models.CharField(max_length = 100, primary_key = True)

class Blog(models.Model):
    blog_url = models.CharField(max_length = 500, primary_key = True)
    blog_author = models.CharField(max_length = 100)
    blog_title = models.TextField()
    blog_published_on = models.DateField()
    blog_modified_on = models.DateField()
    blog_accessed_on = models.DateTimeField(default = timezone.now)
    blog_read_duration = models.CharField(max_length = 20)
    blog_tags = models.ManyToManyField(BlogTag)

    class Meta:
        ordering = ['-blog_accessed_on']

class AccessedTag(models.Model):
    tag_name = models.CharField(max_length = 100, primary_key = True)
    tag_accessed_on = models.DateTimeField(default = timezone.now)
    blogs = models.ManyToManyField(Blog)

    class Meta:
        ordering = ['-tag_accessed_on']