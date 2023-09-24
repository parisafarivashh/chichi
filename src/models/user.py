from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, title, email, password):
        if not email:
            raise ValueError('The Email field must be set')
        if not title:
            raise ValueError('The Title field must be set')

        user = self.model(title=title, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, title, email, password):
        user = self.create_user(
            title=title,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    def user_directory_path(self, filename):
        return f'u{self.id}/avatar/{filename}'

    phone_regex = RegexValidator(regex=r'09(\d{9})$', message="Enter a valid phone_number")
    time_zone_regex = RegexValidator(regex=r'^([+-][0-1]?[0-9]|[+-]2[0-3]):[0-5][0-9]$')
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    phone = models.CharField(max_length=15, validators=[phone_regex])
    email = models.EmailField(unique=True)
    birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_system = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    country_code = models.CharField(max_length=4, null=True, blank=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title']

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'user'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['country_code', 'phone'],
                name='unique_phone',
            )
        ]

