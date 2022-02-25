from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from issuetracking.serializers import (
    UsersSerializer,
    ContributorsSerializer,
    ProjectsSerializer,
    IssuesSerializer,
    CommentsSerializer,
)
from issuetracking.models import Users, Contributors, Projects, Issues, Comments


class UsersViewSet(ModelViewSet):
    serializer_class = UsersSerializer

    def get_queryset(self):
        return Users.objects.all()


class ContributorsViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer

    def get_queryset(self):
        return Contributors.objects.all()


class ProjectsViewSet(ModelViewSet):
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return Projects.objects.all()


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer

    def get_queryset(self):
        return Issues.objects.all()


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.all()
