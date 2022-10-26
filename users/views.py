from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from users.models import User
from .forms import LoginForm, PasswordChangeForm, PasswordResetForm, RegisterForm
from .utils import generate_token

USER = get_user_model()
# USER = settings.AUTH_USER_MODEL


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = USER.objects.get(email=email)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL) # /users/check-user

    return render(request, "registration/login.html", {'form': form})


def logout_view(request):
    print(request.user) # AnonymousUser, <User: Admin>
    if request.user.is_authenticated:
        print('login qilgan')
    else:
        print('nomalum foydalanuvchi')
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def register_view(request):
    form = RegisterForm(request.POST or None) # RegisterForm()

    if request.method == 'POST':
        if form.is_valid():
            fields = form.cleaned_data
            fields['is_active'] = False
            del fields['password_confirmation']
            fields['token_for_activation'] = generate_token(45)       
            user = USER.objects.create_user(**fields)

            # send email to user email for verification
            try:
                email_sent = user.email_user(
                    subject="Verify your email on Havola.uz",
                    message="Please verify your email using this" +
                            f"link http://127.0.0.1:8000/users/{user.id}/verify/{fields['token_for_activation']}" +
                            " to activate your account")
            except Exception as e:
                print(e)
                email_sent = False
            return render(request, 'registration/registration_finish.html', {'email_sent': bool(email_sent)})
    
    return render(request, 'registration/register.html', {'form': form})


def verify_email_view(request, user_id, token):
    user = USER.objects.filter(id=user_id).first()
    if user and user.token_for_activation == token:
        user.is_active = True
        user.token_for_activation = ''
        user.save()
        return render(request, "registration/verify-done.html", {})
    
    return render(request, "registration/verify-fail.html", {})


def password_reset_view(request):
    form = PasswordResetForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            token= default_token_generator.make_token(user)
            # 'domain': domain,
            # 'site_name': site_name,
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # send email to user email for verification
            try:
                email_sent = user.email_user(
                    subject="Password reset email from Havola.uz",
                    message="Please use this link to reset your password" +
                            f"link http://127.0.0.1:8000/users/password-reset-form/{uid}/{token}" +
                            " on Havola.uz")
            except Exception as e:
                print(e)
                email_sent = False
            return render(request, "registration/password-reset-confirm.html")
        else:
            print('Form is invalid')
    # user = USER.objects.filter(id=user_id).first()
    # if user and user.token_for_activation == token:
    #     user.is_active = True
    #     user.token_for_activation = ''
    #     user.save()
    #     return render(request, "registration/verify-done.html", {})
    
    return render(request, "registration/password-reset.html", {'form': form})


def password_reset_form_view(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    token_valid = default_token_generator.check_token(user, token)
    if token_valid:
        form = PasswordChangeForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                new_password = form.cleaned_data['password']
                user.set_password(new_password)
                user.save()
                return HttpResponse("Parol yangilandi!")

        return render(request, "registration/password-change-form.html", {'form': form})

    return HttpResponse('Link invalid')
