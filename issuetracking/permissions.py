from rest_framework.permissions import BasePermission
from issuetracking.models import Projects, Issues, Comments, Contributors


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        if request.resolver_match.kwargs:
            project_id = int(request.resolver_match.kwargs["pk"])
            project = Projects.objects.get(pk=project_id)
            if project.author_user_id.id == user_id:
                return True
            else:
                return False
        else:
            return True


class IsProjectContributor(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        if request.resolver_match.kwargs:
            project_id = int(request.resolver_match.kwargs["pk"])
            project = Contributors.objects.get(project_id=project_id)
            if project.user_id.id == user_id:
                return True
            else:
                return False
        else:
            return True


class IsIssueAuthor(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        if request.resolver_match.kwargs:
            try:
                issue_id = int(request.resolver_match.kwargs["pk"])
                issue = Issues.objects.get(pk=issue_id)
                if issue.author_user_id.id == user_id:
                    return True
                else:
                    return False
            except KeyError:
                return True
        else:
            return True


class IsIssueAssignee(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        print(request.resolver_match.kwargs)
        if request.resolver_match.kwargs:
            print(request.resolver_match.kwargs)
            try:
                issue_id = int(request.resolver_match.kwargs["pk"])
                issue = Issues.objects.get(pk=issue_id)
                if issue.assignee_user_id.id == user_id:
                    return True
                else:
                    return False
            except KeyError:
                return True
        else:
            return True


class IsCommentAuthor(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        comment_id = int(request.resolver_match.kwargs["pk"])
        comment = Comments.objects.get(pk=comment_id)
        if comment.author_user_id.id == user_id:
            return True
        else:
            return False
