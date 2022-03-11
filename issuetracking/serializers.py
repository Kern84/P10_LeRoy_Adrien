from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from issuetracking.models import Users, Contributors, Projects, Issues, Comments


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "first_name", "last_name", "email", "password"]


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ["user_id", "project_id", "permission", "role"]


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author_user_id",
            "contributor",
        ]


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = [
            "id",
            "title",
            "desc",
            "tag",
            "priority",
            "project_id",
            "status",
            "author_user_id",
            "assignee_user_id",
            "created_time",
        ]


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "id",
            "description",
            "author_user_id",
            "issue_id",
            "created_time",
        ]


class LoginSerializer(ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Users
        fields = ["email", "first_name", "last_name", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = Users(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user
