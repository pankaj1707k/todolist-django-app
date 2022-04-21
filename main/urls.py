from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("new-task/", views.TaskCreationView.as_view(), name="new-task"),
    path("tasks/pending/", views.TaskPendingListView.as_view(), name="pending-tasks"),
    path("tasks/edit/<int:pk>/", views.TaskUpdateView.as_view(), name="edit-task"),
    path(
        "tasks/completed/",
        views.TaskCompletedListView.as_view(),
        name="completed-tasks",
    ),
    path("tasks/delete/<int:pk>/", views.TaskDeleteView.as_view(), name="delete-task"),
]
