import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique indentifiers for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and pasword."""
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):

    username = None
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contributors(models.Model):

    PERMISSION_CHOICES = [
        ("AUTHOR", "Author"),
        ("CONTRIBUTOR", "Contributor"),
    ]

    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users",
    )
    project_id = models.ForeignKey(
        "issuetracking.Projects",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=50)

    class Meta:
        unique_together = ("user_id", "project_id")


class Projects(models.Model):

    TYPE_CHOICES = [
        ("BACK-END", "Back-End"),
        ("FRONT-END", "Front-End"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    contributor = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through="Contributors",
        related_name="contributor",
    )

    def __str__(self):
        return self.title


class Issues(models.Model):

    TAG_CHOICES = [("BUG", "Bug"), ("IMPROVEMENT", "Improvement"), ("TASK", "Task")]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    STATUS_CHOICES = [
        ("TO-DO", "To-do"),
        ("IN PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=50, choices=TAG_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(
        "issuetracking.Projects",
        on_delete=models.CASCADE,
        related_name="issues",
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_issues",
    )
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        default=author_user_id,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("title", "project_id")

    def __str__(self):
        return self.title


class Comments(models.Model):
    description = models.CharField(max_length=500)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    issue_id = models.ForeignKey(
        "issuetracking.Issues",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("description", "issue_id")
