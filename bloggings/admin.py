from django.contrib import admin
from bloggings.models import Post
from bloggings.models import Theme
from bloggings.models import Comment

class PostAdmin(admin.ModelAdmin):
    list_diplay = ("title", "content", "theme")

class ThemeAdmin(admin.ModelAdmin):
    list_display = ("id", "label")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "post", "user")

admin.site.register(Post, PostAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Comment, CommentAdmin)
