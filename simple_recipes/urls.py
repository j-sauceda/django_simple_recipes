from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    # user routes
    path('', views.home, name='home'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    # profile routes
    path('update_profile/', views.updateProfile, name='update-profile'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    # article routes
    path('create_article/', views.createArticle, name='create-article'),
    path('article/<str:pk>/', views.readArticle, name='read-article'),
    path('update_article/<str:pk>/',
         views.updateArticle,
         name='update-article'),
    path('delete_article/<str:pk>/',
         views.deleteArticle,
         name='delete-article'),
    # comment routes
    path('create_comment/<str:pk>/',
         views.createComment,
         name='create-comment'),
    path('delete_comment/<str:art_pk>/<str:comm_pk>/',
         views.deleteComment,
         name='delete-comment'),
    # article_picture routes
    path('upload_pictures/<str:pk>/',
         views.uploadPictures,
         name='upload-pictures'),
    path('delete_picture/<str:pk>/',
         views.deletePicture,
         name='delete-picture'),
    # email routes
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name='simple_recipes/reset_password.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='simple_recipes/reset_password_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='simple_recipes/reset_password_form.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='simple_recipes/reset_password_complete.html'),
         name='password_reset_complete'),
]
