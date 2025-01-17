"""
This module defines the migration for adding the `Comment` model to the `blog`
app.

Key additions:
- Introduced the `Comment` model with the following fields:
  - `user_name`: The name of the user making the comment (max 100 characters).
  - `comment_text`: The content of the comment (max 500 characters).
  - `user_email`: The email of the user making the comment.
  - `post`: A foreign key linking the comment to a specific `Post` object in
     the `blog` app.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    A migration that adds the `Comment` model to the `blog` app.

    The `Comment` model includes:
    - `user_name`: The name of the commenter.
    - `comment_text`: The actual text of the comment.
    - `user_email`: The commenter's email for identification or notifications.
    - `post`: A foreign key to the `Post` model, enforcing a `CASCADE` delete
              rule to remove comments when a post is deleted.
    """

    dependencies = [
        ("blog", "0002_remove_post_image_name_post_image_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_name", models.CharField(max_length=100)),
                ("comment_text", models.TextField(max_length=500)),
                ("user_email", models.EmailField(max_length=254)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="blog.post",
                    ),
                ),
            ],
        ),
    ]
