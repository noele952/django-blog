"""
This module defines the application configuration for the 'blog' module
in the Django project. The configuration specifies default behavior
and metadata for the app, such as its name and default auto field type.
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Configuration class for the 'blog' application in the Django project.

    This class specifies:
    - The name of the app ('blog').
    - The default auto field type for models in this app, which is set to
      'django.db.models.BigAutoField'. This ensures that primary keys
      use a 64-bit integer field by default.

    Attributes:
        default_auto_field (str): The default field type for auto-incrementing
            primary keys in models.
        name (str): The name of the application as it appears in project
        settings.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
