from django.contrib import admin
from .models import Blog, AccessedTag, BlogTag

admin.site.register(Blog)
admin.site.register(BlogTag)
admin.site.register(AccessedTag)
