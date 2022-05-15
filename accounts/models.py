from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from base.services import get_path_upload_avatar, validate_size_image, get_default_avatar


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, gender, date_of_birth, avatar=get_default_avatar(), password=None, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, gender=gender, avatar=avatar, date_of_birth=date_of_birth, is_superuser=is_superuser)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, gender, date_of_birth, password=None, **kwargs):
        user = self.create_user(
            email,
            name=name,
            gender=gender,
            date_of_birth=date_of_birth,
            password=password,
            is_superuser=True,
            **kwargs,
        )
        user.staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=10, default='01.01.2000')
    gender = models.CharField(max_length=1, default='M')

    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        default=get_default_avatar(),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']), validate_size_image]
    )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'gender', 'date_of_birth', 'avatar']

    @property
    def is_authenticated(self):
        return True

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
