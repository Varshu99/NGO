from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
        path('',views.home, name="home" ),
        path('submit-valunteer',views.submit_valunteer, name="submit-valunteer" ),
        path('contact',views.contact, name="contact" ),
        path('donate/<int:id>',views.donate, name="donate" ),
        path('signup/', views.signup_view, name='signup'),
        path('signin', views.signin_view, name='signin'),
        path(
        "request_password_reset/",
        views.request_password_reset,
        name="request_password_reset",
    ),
        path("reset_password/<uname>/", views.reset_password, name="reset_password"),
        path("logout", views.logout_view, name="logout"),  # Logout page


]
