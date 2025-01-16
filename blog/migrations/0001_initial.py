"""
Migration module for creating the initial database schema for the blog app.

This migration creates three models:
1. Author: A model representing authors, including fields for first name,
   last name, and email.
2. Tag: A model representing tags used to categorize blog posts.
3. Post: A model representing individual blog posts, including fields for
   title, excerpt, content, and relations to Author and Tag models.

It also includes related migration operations to set up the relationships
and structure of the database.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    A migration class for creating the initial set of database models for the
    blog app.

    This migration contains the creation of:
    - Author model with `first_name`, `last_name`, and `e_mail` fields.
    - Tag model with a `caption` field.
    - Post model with fields for `title`, `excerpt`, `image_name`, `date`,
      `slug`, and `content`, and foreign key relationships to Author and Tag
      models.
    """

    initial = True

    dependencies: list = [
        # List the dependencies for this migration, if any.
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('e_mail', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('caption', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('excerpt', models.CharField(max_length=1000)),
                ('image_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('slug', models.SlugField(blank=True, default='')),
                ('content', models.CharField(max_length=10000)),
                ('author', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='posts',
                    to='blog.author')),
                ('tag', models.ManyToManyField(related_name='posts',
                                               to='blog.tag')),
            ],
        ),
    ]
