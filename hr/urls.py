"""hr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.contrib import admin
from django.urls import path, include


schema_view = get_schema_view(
   openapi.Info(
      title="MUGNA-HR API",
      default_version="v1",
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        r"api/",
        include(
            [
                path(r"docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs"),
                path(r"", include("django.contrib.auth.urls")),
                path(r"auth/", include(("rest_auth.urls")),),
                path(
                    r"v1/users/",
                    include(("users.api.v1.urls", "users"), namespace="users-v1"),
                ),
                path(
                    r"v1/employees/",
                    include(
                        ("employees.api.v1.urls", "employees"), namespace="employees-v1"
                    ),
                ),
                path(
                    r"v1/leaves/",
                    include(("leaves.api.v1.urls", "leaves"), namespace="leaves-v1"),
                ),
            ],
        ),
    ),
]
