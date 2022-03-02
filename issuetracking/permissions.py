from rest_framework.permissions import BasePermission
from issuetracking.models import Projects, Users, Contributors


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        project_id = Projects.objects.get(id=view.kwargs["pk"])
        print(project_id)
        print(project_id.author_user_id)
        user_id = Users.objects.get(id=request.user.id)
        print(user_id)
        if request.user == project_id.author_user_id:
            print("author")
        else:
            self.message = "You cannot edit this project."
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user == project_id.author_user_id
        )
