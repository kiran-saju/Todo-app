from django.urls import path
from todoapp.views import TaskList,TaskDetails,TaskCreate,TaskUpdate,TaskDelete,CustomLoginView,CustomLogoutView,RegisterPage
# from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('',TaskList.as_view(),name="task"),
    path('task/<int:pk>/',TaskDetails.as_view(),name="task-details"),
    path('task-create/',TaskCreate.as_view(),name="task-create"), 
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name="task-update"),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name="task-delete"),
    path('login/',CustomLoginView.as_view(),name="login"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/',RegisterPage.as_view(),name="register"),
]
