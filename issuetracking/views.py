from rest_framework.viewsets import ModelViewSet
from issuetracking.serializers import (
    UsersSerializer,
    ContributorsSerializer,
    ProjectsSerializer,
    IssuesSerializer,
    CommentsSerializer,
    LoginSerializer,
)
from issuetracking.models import Users, Contributors, Projects, Issues, Comments
from rest_framework.response import Response
from rest_framework.decorators import api_view
from issuetracking.permissions import (
    IsProjectAuthor,
    IsProjectContributor,
    IsIssueAuthor,
    IsCommentAuthor,
)
from rest_framework.permissions import IsAuthenticated


class UsersViewSet(ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Users.objects.all()


class ContributorsViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Contributors.objects.all()


class ProjectsViewSet(ModelViewSet):
    serializer_class = ProjectsSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated()]

        if self.request.method == "GET":
            permission_classes = [
                IsProjectContributor(),
                IsAuthenticated(),
            ]
        elif self.request.method == "DELETE" or self.request.method == "PUT":
            permission_classes = [IsProjectAuthor(), IsAuthenticated()]

        return permission_classes

    def get_queryset(self):
        user = self.request.user.id
        return Projects.objects.filter(author_user_id=user) | Projects.objects.filter(
            contributor=user
        )


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer

    def get_permissions(self):
        permission_classes = [
            IsAuthenticated(),
        ]

        if self.request.method == "GET":
            permission_classes = [
                IsProjectContributor(),
                IsAuthenticated(),
            ]
        elif self.request.method == "DELETE" or self.request.method == "PUT":
            permission_classes = [
                IsIssueAuthor(),
                IsAuthenticated(),
            ]
        elif self.request.method == "POST":
            permission_classes = [
                IsProjectContributor(),
                IsAuthenticated(),
            ]

        return permission_classes

    def get_queryset(self):
        user = self.request.user.id
        return Issues.objects.filter(project_id=self.kwargs["project_pk"]).filter(
            author_user_id=user
        ) | Issues.objects.filter(project_id=self.kwargs["project_pk"]).filter(
            assignee_user_id=user
        )


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_permissions(self):
        permission_classes = [
            IsAuthenticated(),
        ]

        if self.request.method == "GET":
            permission_classes = [
                IsProjectContributor(),
                IsAuthenticated(),
            ]
        elif self.request.method == "DELETE" or self.request.method == "PUT":
            permission_classes = [
                IsCommentAuthor(),
                IsAuthenticated(),
            ]
        elif self.request.method == "POST":
            permission_classes = [
                IsProjectContributor(),
                IsAuthenticated(),
            ]

        return permission_classes

    def get_queryset(self):
        user = self.request.user.id
        return Comments.objects.filter(issue_id=self.kwargs["issue_pk"]).filter(
            author_user_id=user
        )


@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["response"] = "Successfully register a new user."
            data["email"] = user.email
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name
        else:
            data = serializer.errors
        return Response(data)
