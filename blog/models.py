from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator


# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    e_mail = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Post(models.Model):
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
        return reverse("post-detail", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    comment_text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
