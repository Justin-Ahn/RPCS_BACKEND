from django.urls import path
from user import views


urlpatterns = [
    path("login", views.login_action, name="login"),
    path("logout", views.logout_action, name="logout"),
    path("register", views.register_action, name="register"),
    path("myprofile", views.view_profile_action, name="myprofile"),
    path("edit-profile", views.edit_profile_action, name="edit-profile"),
    path("myaddress", views.view_address_action, name="myaddress"),
    path("edit-address", views.edit_address_action, name="edit-address"),
    path("activate/<code>", views.activate_action, name="activate"),
    path("reset/<code>", views.get_reset_action, name="reset"),
    path("update/", views.update_pwd_action, name="update-pwd"),
    path("forget/", views.forget_pwd_action, name="forget"),
]