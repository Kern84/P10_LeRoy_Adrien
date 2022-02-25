from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from issuetracking.models import Users, Contributors, Projects, Issues, Comments


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_id", "first_name", "last_name", "email", "password"]


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ["user_id", "project_id", "permission", "role"]


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = [
            "title",
            "desc",
            "tag",
            "priority",
            "project_id",
            "status",
            "author_user_id",
            "assignee_user_id",
        ]


class ProjectsSerializer(ModelSerializer):

    issues = IssuesSerializer(many=True)

    class Meta:
        model = Projects
        fields = [
            "project_id",
            "title",
            "description",
            "type",
            "author_user_id",
            "issues",
        ]


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "comment_id",
            "description",
            "author_user_id",
            "issue_id",
        ]
