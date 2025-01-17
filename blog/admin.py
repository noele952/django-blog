"""
This module configures the admin interface for the blog application.

It includes custom admin configurations for the `Post` and `Comment` models
to enhance the user experience for site administrators.

The following customizations are applied:
    - `PostAdmin`: Configures the display and filters for blog posts.
    - `CommentAdmin`: Configures the display and filters for comments.

Additionally, the `Author`, `Tag`, `Post`, and `Comment` models are registered
with the Django admin site to make them accessible and manageable through the
admin interface.
"""

from django.contrib import admin
from .models import Post, Author, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.

    This class customizes the admin interface for managing blog posts.
    It prepopulates the slug field from the title and provides filtering
    options by author, date, and tags. It also defines how the posts are
    displayed in the list view (title, date, and author).
    """

    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author", "date", "tag")
    list_display = ("title", "date", "author")


class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.

    This class customizes the admin interface for managing comments.
    It defines how comments are displayed in the list view (user name and
    associated post), and allows filtering comments by user name and
    associated post.
    """

    list_display = ("user_name", "post")
    list_filter = ("user_name", "post")


# Register the models with the admin interface
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
