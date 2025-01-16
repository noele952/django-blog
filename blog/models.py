"""
This module defines the models for the blog application, including `Author`,
`Tag`, `Post`, and `Comment`. Each model represents an important entity in
the blogging system and is used to interact with the database to store relevant
information about authors, posts, comments, and tags.

Models:
    - `Author`: Stores details about blog authors such as name and email.
    - `Tag`: Represents tags associated with blog posts.
    - `Post`: Contains the details of individual blog posts including content,
      title, and author.
    - `Comment`: Stores user comments on posts, including user details and
      comment text.
"""

from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator


class Author(models.Model):
    """
    Model representing a blog post author.

    The Author model stores the first and last name of the author, along with
    their email address. It also provides a method to return the full name of
    the author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    e_mail = models.EmailField()

    def full_name(self):
        """
        Returns the full name of the author in the format 'first_name
        last_name'.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        Returns the full name of the author as a string representation.
        """
        return self.full_name()


class Tag(models.Model):
    """
    Model representing a tag used to categorize blog posts.

    The Tag model contains a single field for the caption of the tag and
    provides a method to represent the tag as a string.
    """
    caption = models.CharField(max_length=20)

    def __str__(self):
        """
        Returns the caption of the tag as a string representation.
        """
        return self.caption


class Post(models.Model):
    """
    Model representing a blog post.

    The Post model includes essential fields like title, excerpt, image,
    content, and tags. It defines relationships to the `Tag` model
    (many-to-many) and the `Author` model (foreign key). Additionally,
    a method for generating the absolute URL for a post is provided.
    """
    title = models.CharField(max_length=255)
    excerpt = models.CharField(max_length=400)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    tag = models.ManyToManyField(Tag, related_name="posts")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,
                               related_name="posts")

    def get_absolute_url(self):
        """
        Returns the URL for the detailed view of the post.
        """
        return reverse("post-detail", args=[self.slug])

    def __str__(self):
        """
        Returns the title of the post as its string representation.
        """
        return self.title


class Comment(models.Model):
    """
    Model representing a comment on a blog post.

    The Comment model includes the user's name, email, the text of their
    comment, and a relationship to the `Post` model to associate the comment
    with a specific blog post.
    """
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    comment_text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
