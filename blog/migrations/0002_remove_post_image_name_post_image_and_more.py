"""
This module contains a migration for the `blog` app.

Key modifications made in this migration:
- **Post Model**:
  1. Replaced `image_name` field with `ImageField` for file uploads.
  2. Updated the `author` field to use `SET_NULL` on deletion while retaining
     `related_name='posts'`.
  3. Added a minimum length validator of 10 characters to the `content` field.
  4. Set the `date` field to automatically update to the current date.
  5. Shortened the maximum length of `excerpt` to 400 characters.
  6. Set the `slug` field to be unique.
- **Author Model**:
  1. Updated the `e_mail` field to use `EmailField` for validation.
- **Tag Model**:
  1. Shortened the maximum length of `caption` to 20 characters.
"""

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Represents the migration operations for the `blog` app.

    This migration adjusts schema and validations for models including:
    - `Author` with a more specific email validation.
    - `Post` with updated field properties such as `slug`, `excerpt`,
      `content`, `author`, `date`, and new support for image uploads.
    - `Tag` with a reduced `caption` maximum length.
    """

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="image_name",
        ),
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(null=True, upload_to="posts"),
        ),
        migrations.AlterField(
            model_name="author",
            name="e_mail",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to="blog.author",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(
                validators=[django.core.validators.MinLengthValidator(10)]
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="date",
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="excerpt",
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name="tag",
            name="caption",
            field=models.CharField(max_length=20),
        ),
    ]
