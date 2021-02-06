from django.urls import path
from .import views
urlpatterns = [
    path('',views.Home),
    path('login/',views.LoginView,name="login"),
    path('logout/',views.Logout,name="logout"),
    path('dashboard/',views.Dashboard,name="dash"),
    path('user-list/',views.UserList,name="userlist"),
    path('update/<int:id>',views.Update,name="update"),
    path('delete/<int:id>',views.Delete,name="delete"),
]
