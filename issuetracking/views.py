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
    IsIssueAssignee,
    IsCommentAuthor,
)
from rest_framework.permissions import IsAuthenticated


class UsersViewSet(ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Users.objects.all()


class ContributorsViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributors.objects.all()


class ProjectsViewSet(ModelViewSet):
    serializer_class = ProjectsSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated()]

        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated() and (IsProjectAuthor() or IsProjectContributor())
            ]
        elif self.request.method == "DELETE" or self.request.method == "PUT":
            permission_classes = [IsAuthenticated() and IsProjectAuthor()]

        return permission_classes

    def get_queryset(self):
        user = self.request.user.id
        return Projects.objects.filter(author_user_id=user) | Projects.objects.filter(
            contributor=user
        )


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated()]

        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated()
                and (
                    IsIssueAuthor()
                    or IsIssueAssignee()
                    or IsProjectAuthor()
                    or IsProjectContributor()
                )
            ]
        elif self.request.method == "DELETE" or self.request.method == "PUT":
            permission_classes = [IsAuthenticated() and IsIssueAuthor()]
        elif self.request.method == "POST":
            permission_classes = [
                IsAuthenticated() and (IsProjectAuthor() or IsProjectContributor())
            ]

        return permission_classes

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs["project_pk"])


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated()]

        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated()
                and (IsCommentAuthor() or IsProjectAuthor() or IsProjectContributor())
            ]
        elif self.request.method == "DELETE" or self.request.method == "PUT":
            permission_classes = [IsAuthenticated() and IsCommentAuthor()]
        elif self.request.method == "POST":
            permission_classes = [
                IsAuthenticated() and (IsProjectAuthor() or IsProjectContributor())
            ]

        return permission_classes

    def get_queryset(self):
        user = self.request.user.id
        return Comments.objects.filter(author_user_id=user)


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
