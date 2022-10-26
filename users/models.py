from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    UserManager
)
from django.conf import settings
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):

    # def create_user(self, ):
    #     pass

    # def create_superuser(self, ):
    #     pass 

    def create_user(self, email, password=None, **extra_fields): # **kwargs
        
        email = self.normalize_email(email)
        # user.is_active = False
        # user.is_staff = False
        # user.is_superuser = False
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model.objects.create(email=email, **extra_fields) # create(email=email, a=1, b=2)
        if password:
            user.set_password(password)
            user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField('Email address', unique=True)
    is_staff = models.BooleanField(default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField('active', default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField('Date joined', auto_now_add=True)
    token_for_activation = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email' # null=False, unique=True

    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager() # objects.create() create_user()

    def email_user(self, subject, message, **kwargs):
        return send_mail(
            subject=subject,
            message=message,
            html_message=kwargs.get('html_message', None),
            recipient_list=[self.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            fail_silently=kwargs.get('fail_silently', True)
        )

class BookmarkedLink(models.Model):
    STATUS = (
        ('L', "O'qiyapman"),
        ('W', "O'rganishni xohlayman"),
        ('K', "Bilaman")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')   # user.bookmarks.
    link = models.ForeignKey("core.GeneralLink", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0][0])
    created_at = models.DateTimeField(auto_now_add=True)