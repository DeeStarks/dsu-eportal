"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
import portal.views as portal
import timetable.views as timetable
import post_creation.views as post
import library.views as library
import authentication.views as authentication
import courses.views as courses
import assessment.views as assessment
from django.contrib.auth import views as auth_views


admin.site.site_header = "DeeStarks University Admin"
admin.site.site_title = "DSU Admin Portal"
admin.site.index_title = "Welcome to DeeStarks University Portal"

urlpatterns = [
    path('administration/', admin.site.urls),
    path("authenticate", authentication.login_user, name="authentication"),

    # Password Reset URLs
    path(
        'password/reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
        name='reset_password'
    ),
    path(
        'password/reset/sent', 
        auth_views.PasswordResetDoneView.as_view(template_name='reset_sent.html'), 
        name='password_reset_done'
    ),
    path(
        'password/reset/<uidb64>/<token>', 
        auth_views.PasswordResetConfirmView.as_view(template_name='reset_form.html'), 
        name='password_reset_confirm'
    ),
    path(
        'password/reset/complete', 
        auth_views.PasswordResetCompleteView.as_view(template_name='reset_complete.html'), 
        name='password_reset_complete'
    ),

    # Main Contents URLs
    path("", portal.index, name="home"),
    path("admin/pr/", include("portal.urls")),
    path("user/", include("user_profile.urls")),
    path("admin/tt/", include("timetable.urls")),
    path("table", timetable.timetable, name="table"),
    path("post/<str:post_id>/<str:title>", post.posts, name="post page"),
    path("admin/p/", include("post_creation.urls")),
    path("admin/c/", include("courses.urls")),
    path("staff/allocated-courses", courses.allocated_course, name="allocated courses"),
    path("admin/library/", include("library.urls")),
    path("admin/ss/", include("session_semester.urls")),
    path("library", library.library, name="library"),
    path("admin/user/add", authentication.create_user, name="register"),
    path("logout", authentication.logout_user, name="logout"),
    path("admin/sm/mastersheet", assessment.mastersheet, name="mastersheet"),
    path("admin/sm/mastersheet/download/<str:department>/<str:level>", assessment.mastersheet_template, name="mastersheet template"),
    path("staff/scoresheet", assessment.scoresheet, name="scoresheet"),
    path("staff/scoresheet/upload/<str:course_code>", assessment.scoresheet_upload, name="scoresheet upload"),
    path("staff/scoresheet/download/<str:course_code>", assessment.scoresheet_download, name="scoresheet download"),
    path("courses", courses.courses, name="courses"),
    path("records", assessment.records, name="records"),
    path("result", assessment.result, name="result"),
    path("password/change", portal.change_password, name="change password"),
    path("attendance", portal.attendance, name="attendance"),

    path("start", portal.get_started, name="start"),
    path("<str:url>", portal.page404, name="error404"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
