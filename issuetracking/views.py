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
from rest_framework import status


class UsersViewSet(ModelViewSet):
    """View the users."""

    serializer_class = UsersSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Users.objects.all()


class ContributorsViewSet(ModelViewSet):
    """
    View the contributors of a project.
    Functions to create and destroy contributors in the right project.
    """

    serializer_class = ContributorsSerializer
    permission_classes = [
        IsProjectAuthor,
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Contributors.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ContributorsSerializer(data=request.data)
        instance_project = Projects.objects.get(id=kwargs["project_pk"])
        perso = Users.objects.get(id=request.data["user_id"])
        if serializer.is_valid():
            serializer.save(
                project_id=instance_project,
                user_id=perso,
                role="Contributor",
                permission="CONTRIBUTOR",
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        project_instance = Projects.objects.get(id=kwargs["project_pk"])
        user_instance = Users.objects.get(id=kwargs["pk"])
        obj = Contributors.objects.filter(project_id=project_instance).filter(
            user_id=user_instance
        )
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = "The contributor was successfully deleted "
        return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)


class ProjectsViewSet(ModelViewSet):
    """
    View the projects of which you are a contributor.
    Function to add the project's author as a contributor.
    """

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
        return Projects.objects.filter(contributor=user)

    def create(self, request, *args, **kwargs):
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author_user_id=request.user)
            contributor = Contributors.objects.create(
                project_id=project,
                user_id=request.user,
                role="Author",
                permission="AUTHOR",
            )
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssuesViewSet(ModelViewSet):
    """
    View for the issues of a project.
    Function to create an issue in the right project.
    """

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
        return Issues.objects.filter(project_id=self.kwargs["project_pk"])

    def create(self, request, *args, **kwargs):
        project = Projects.objects.get(id=kwargs["project_pk"])
        serializer = IssuesSerializer(data=request.data)
        assignee = Users.objects.get(id=request.data["assignee_user_id"])
        if (
            Contributors.objects.filter(user_id=assignee)
            .filter(project_id=project)
            .exists()
        ):
            if serializer.is_valid():
                serializer.save(author_user_id=request.user, project_id=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            message = "The assignee user is not yet a contributor to this project"
            return Response({"message": message}, status=status.HTTP_200_OK)


class CommentsViewSet(ModelViewSet):
    """
    View for comments in an issue.
    Function to create a comment in the right issue.
    """

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
        return Comments.objects.filter(issue_id=self.kwargs["issue_pk"])

    def create(self, request, *args, **kwargs):
        issue_obj = Issues.objects.get(id=kwargs["issue_pk"])
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(issue_id=issue_obj, author_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def registration_view(request):
    """
    Function to create a new user.
    """
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
