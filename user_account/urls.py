from django.urls import path 
from . import views
urlpatterns = [
    path('register',views.UserRegisterView.as_view(),name='register'),
    path('activate/<str:uidb64>/<str:token>',views.ActivationConfirmView.as_view(),name='activate'),
    path('signin',views.UserSigninView.as_view(),name='signin'),
    path('profile',views.ProfileView.as_view()),
    path('refresh',views.RefreshTokenView.as_view()),
    path('reset-password',views.ResetPasswordView.as_view()),
    path('confirm-reset-password/<str:uidb64>/<str:token>',views.ConfirmResetPassword.as_view(),name='confirm_password'),
    path('logout',views.LogoutView.as_view())

]
