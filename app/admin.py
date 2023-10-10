from django.contrib import admin
from app.models import BlogPost
from app.models import Profile
from app.models import Comment

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','user','subtitle','dateTime')

admin.site.register(BlogPost,BlogPostAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','facebook','twitter','github')

admin.site.register(Profile,ProfileAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','comment')
admin.site.register(Comment,CommentAdmin)
