from django.contrib import admin

from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date')
    list_display_links = ('pk', 'text')
    search_fields = ('text', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    list_display_links = ('pk', 'title')
    search_fields = ('description', 'title')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author')
    list_display_links = ('pk', 'author')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_display_links = ('pk', 'user', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)