from django.contrib import admin
from .models import Post, Emoji, Sticker, Category, Tag, Comment

admin.site.register(Post)
admin.site.register(Emoji)
admin.site.register(Sticker)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
