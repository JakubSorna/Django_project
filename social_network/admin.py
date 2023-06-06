from django.contrib import admin
from .models import Profile, Post, Comment_post, Comment_photo, Photo

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment_post)
admin.site.register(Comment_photo)
admin.site.register(Photo)