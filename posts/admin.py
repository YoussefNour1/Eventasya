from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ['content']
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['id', 'post', 'commenter', 'content', 'created_at']
    readonly_fields = ['post', 'commenter', 'content', 'created_at']

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'user', 'content', 'created_at']
    readonly_fields = ['user', 'content', 'created_at']
    inlines = [CommentInline]

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user == obj.user:
            return True
        return False


