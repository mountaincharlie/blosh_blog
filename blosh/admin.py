from django.contrib import admin
from .models import Blog, Comment
from django_summernote.admin import SummernoteModelAdmin

# customising the blog search/editing section - registering with a decorator
@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    # to allow customazability in the 'content' field of the blog
    summernote_fields = ('content')

    # auto generating the slug field from title
    prepopulated_fields = {
        'slug': ('title',)  # tuple
    }

    # info to be displayed in blogs list
    list_display = ('title', 'created_date', 'status')

    # give admin filtering functionalilty for the blogs
    list_filter = ('status', 'title', 'created_date')

    # fields to search by
    search_fields = ('title', 'content', 'status')


# customising the comments viewing/approving section
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    # how it looks
    list_display = ('blog', 'name', 'created_date', 'approved')
    list_filter = ('approved', 'blog', 'created_date', 'name')
    search_fields = ('name', 'blog', 'body', 'created_date', 'approved')

    # which of this class's methods to allow as actions
    actions = ['approve_comment', 'block_comment']

    # changing the approved status to True
    def approve_comment(self, request, queryset):
        queryset.update(approved=True)
    
    # changing the approved status to False
    def block_comment(self, request, queryset):
        queryset.update(approved=False)
