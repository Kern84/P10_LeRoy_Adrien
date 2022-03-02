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
from issuetracking.permissions import IsProjectAuthor


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
    # permission_classes = [IsProjectAuthor]

    def get_queryset(self):
        author = self.request.GET.get("author_user_id")
        queryset = Projects.objects.filter(author_user_id=author)
        return Projects.objects.all()
        # return queryset


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer

    def get_queryset(self):
        return Issues.objects.all()


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.all()


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
