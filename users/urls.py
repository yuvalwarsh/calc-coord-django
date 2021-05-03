from django.urls import path
from . import views as users_views

urlpatterns = [
    path('register/', users_views.register, name='register'),
    path('login/', users_views.LoginFormView.as_view(), name="login"),
    path('logout/', users_views.logout_view, name="logout"),
    path('password-reset/', users_views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', users_views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', users_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', users_views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete')
]
