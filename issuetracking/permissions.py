from rest_framework.permissions import BasePermission
from issuetracking.models import Projects, Users, Contributors


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        user = request.user.id
        author = Projects.objects.filter(author_user_id=user)
        return bool(request.user and request.user.is_authenticated and author)


class IsProjectContributor(BasePermission):
    def has_permission(self, request, view):
        user = request.user.id
        contributor = Projects.objects.filter(contributor=user)
        return bool(request.user and request.user.is_authenticated and contributor)
