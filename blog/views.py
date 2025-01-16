"""
This module contains views for the 'blog' application in the Django project.

It defines various views related to blog posts, including displaying the
starting page with recent posts, viewing all posts, detailed views of
individual posts, and a read-later functionality to store and view posts.
"""

from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .forms import CommentForm


class StartingPageView(ListView):
    """
    View for rendering the starting page with a list of recent blog posts.

    This class-based view uses Django's ListView to display a list of the most
    recent posts. The queryset is customized to display only the latest 3
    posts.

    Attributes:
        template_name (str): The template to render the list of posts.
        model (class): The model from which to retrieve data (Post).
        context_object_name (str): The name used for the posts variable in the
        template.
        ordering (list): The ordering of posts, with most recent first.

    Methods:
        get_queryset: Limits the displayed posts to the top 3 most recent
        posts.
    """
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]

    def get_queryset(self):
        """
        Custom queryset method to retrieve only the top 3 recent posts.

        This method overrides the default queryset behavior to limit the number
        of posts shown on the starting page to the three most recent ones.

        Returns:
            Queryset: A limited set of the three most recent posts.
        """
        base_query = super().get_queryset()
        data = base_query[:3]
        return data


class PostsView(ListView):
    """
    View for rendering a list of all blog posts.

    This class-based view is used to display all the posts from the blog. The
    posts are ordered by date in descending order, and the queryset does not
    need to be customized as it retrieves all available posts.

    Attributes:
        template_name (str): The template to render the list of all posts.
        model (class): The model from which to retrieve data (Post).
        ordering (list): The ordering of posts, with most recent first.
        context_object_name (str): The name used for the all_posts variable in
        the template.
    """
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class PostDetailView(View):
    """
    View for displaying the detailed view of a single post.

    This view handles both GET and POST requests for displaying a specific blog
    post, its associated tags, comments, and handling the submission of new
    comments.

    Attributes:
        None explicitly defined.

    Methods:
        get: Renders the post detail page with tags, comments, and a comment
        form.
        post: Handles form submission for adding a new comment and redirects
        on success.
        is_stored_post: Checks if the post is stored for later in the user's
        session.
    """

    def is_stored_post(self, request, post_id):
        """
        Checks if the post is stored for later in the session.

        This method checks whether the specified post has been marked as
        'saved for later' in the user's session data.

        Args:
            request (HttpRequest): The HTTP request object.
            post_id (int): The ID of the post to check.

        Returns:
            bool: True if the post is stored for later, otherwise False.
        """
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        """
        Handles GET requests to render a post detail page.

        Retrieves the blog post based on the slug, renders the post with its
        comments and a comment form, and also checks if the post is stored
        for later.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the post to retrieve.

        Returns:
            HttpResponse: The rendered post detail page.
        """
        post = Post.objects.get(slug=slug) # pylint: disable=no-member
        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }

        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug): # pylint: disable=no-member
        """
        Handles POST requests to submit a new comment on a post.

        Validates the submitted comment form, saves the comment if valid, and
        redirects
        to the post detail page.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the post to add the comment to.

        Returns:
            HttpResponseRedirect: Redirects to the post detail page after
            saving the comment.
        """
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page",
                                                args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }

        return render(request, "blog/post-detail.html", context)


class ReadLaterView(View):
    """
    View for handling storing and retrieving posts marked as 'saved for later'.

    This view allows users to see a list of posts they've saved for later, and
    also add or remove posts from that list.

    Attributes:
        None explicitly defined.

    Methods:
        get: Renders a list of saved posts.
        post: Adds or removes a post from the user's saved posts list in the
        session.
    """

    def get(self, request):
        """
        Handles GET requests to display a list of stored posts.

        Retrieves the list of saved posts from the user's session and renders
        them on a dedicated page. If no posts are saved, it provides a message
        indicating that the list is empty.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered stored posts page.
        """
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts) # pylint: disable=no-member
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        """
        Handles POST requests to save or remove posts from the saved list.

        This method updates the user's session to either add or remove a post
        from their saved posts list and then redirects to the home page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the home page after updating
            the session.
        """
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
