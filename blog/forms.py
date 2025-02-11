"""
This module defines the form used for submitting comments on blog posts.

It contains the `CommentForm`, a Django model form for the `Comment` model.
The form allows users to enter their name, email, and comment text when
submitting a comment on a blog post. The 'post' field is excluded from the
form to ensure it is automatically set based on the associated blog post.

Fields in the form include:
    - user_name: The name of the user submitting the comment.
    - user_email: The email address of the user submitting the comment.
    - comment_text: The content of the comment.

The form uses custom labels for each field to improve user experience.
"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    A form for creating and submitting comments on blog posts.

    This form is connected to the Comment model and excludes the 'post' field
    to ensure that the associated post is set programmatically. The form allows
    users to provide their name, email, and comment text. The 'user_name',
    'user_email', and 'comment_text' fields are customized with specific
    labels.
    """

    class Meta:
        # pylint: disable=too-few-public-methods
        """
        Metadata for the CommentForm class.

        This inner class provides configuration options for the form.
        Specifically, it:
        - Specifies the associated model as 'Comment', allowing the form to be
          directly tied to the database model.
        - Excludes the 'post' field, ensuring that the post association is
          handled programmatically rather than by user input.
        - Customizes the labels for form fields, providing user-friendly names
          for:
            - 'user_name': Displayed as "Your Name".
            - 'user_email': Displayed as "Your Email".
            - 'comment_text': Displayed as "Your Comment".
        """
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "comment_text": "Your Comment",
        }
