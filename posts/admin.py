from django.contrib import admin

from posts.models import Post, Category


class CategoryPostAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'author', 'category', 'status')


class PostReview(admin.ModelAdmin):
    list_display = ('post', 'user', 'review_text')


admin.site.register(Category, CategoryPostAdmin)
admin.site.register(Post, PostAdmin)