from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path("", views.login_page, name="login"),
    path("login/", views.login_page, name="login"),
    path("home/", views.home, name="home"),
    path("create_account/", views.create_account, name="create_account"),
    path("auth_user/", views.auth_user, name="auth_user" ),
    path('logout/', LogoutView.as_view(),{'next_page': settings.LOGOUT_REDIRECT_URL}, name = "logout"),
    path("book_table/", views.book_table, name="book_table")
]