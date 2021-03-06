"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from issuetracking.views import (
    UsersViewSet,
    ContributorsViewSet,
    ProjectsViewSet,
    IssuesViewSet,
    CommentsViewSet,
    registration_view,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.SimpleRouter()
router.register("users", UsersViewSet, basename="users")
router.register("contributors", ContributorsViewSet, basename="contributors")
router.register("projects", ProjectsViewSet, basename="projects")
router.register("issues", IssuesViewSet, basename="issues")
router.register("comments", CommentsViewSet, basename="comments")

project_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
project_router.register("issues", IssuesViewSet, basename="issues")
project_router.register("users", ContributorsViewSet, basename="users")

comment_router = routers.NestedSimpleRouter(project_router, r"issues", lookup="issue")
comment_router.register("comments", CommentsViewSet, basename="comments")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("api/", include(project_router.urls)),
    path("api/", include(comment_router.urls)),
    path("api/login/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("api/signup/", registration_view, name="signup"),
]
