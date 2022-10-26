from django.urls import path
from .views import (login_view, logout_view, register_view,
verify_email_view, password_reset_view, password_reset_form_view)
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

urlpatterns = [
    path('password-reset', password_reset_view),
    path('custom-login', login_view, name='login'),
    path('custom-logout', logout_view),
    path('custom-register', register_view),
    path('<int:user_id>/verify/<str:token>', verify_email_view, name='verify-email'),
    path('password-reset-form/<str:uidb64>/<str:token>', password_reset_form_view)
]

# href='users/12/verify/asdnuqweakjshkjasdh
# {% url 'verify-email' user_id=12 token=asdnuqweakjshkjasdh %}
