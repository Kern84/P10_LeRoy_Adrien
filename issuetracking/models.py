from django.db import models


class Users(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=50, unique=True)


class Contributors(models.Model):

    PERMISSION_CHOICES = [
        ("AUTHOR", "Author"),
        ("CONTRIBUTOR", "Contributor"),
    ]

    user_id = models.ForeignKey(
        "issuetracking.Users",
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


class Projects(models.Model):

    TYPE_CHOICES = [
        ("BACK-END", "Back-End"),
        ("FRONT-END", "Front-End"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    project_id = models.IntegerField()
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(
        "issuetracking.Users",
        on_delete=models.CASCADE,
        related_name="projects",
    )


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
        "issuetracking.Users",
        on_delete=models.CASCADE,
        related_name="created_issues",
    )
    assignee_user_id = models.ForeignKey(
        "issuetracking.Users",
        default=author_user_id,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=500)
    author_user_id = models.ForeignKey(
        "issuetracking.Users",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    issue_id = models.ForeignKey(
        "issuetracking.Issues",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_time = models.DateTimeField(auto_now_add=True)
