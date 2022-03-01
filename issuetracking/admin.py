from django.contrib import admin
from issuetracking.models import Users, Contributors, Projects, Issues, Comments


class IssueAdmin(admin.ModelAdmin):
    list_display = ("title",)


class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "project_id",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("description",)


admin.site.register(Users)
admin.site.register(Contributors, ContributorAdmin)
admin.site.register(Projects)
admin.site.register(Issues, IssueAdmin)
admin.site.register(Comments, CommentAdmin)
