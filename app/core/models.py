import uuid
import os
from django.db import models as md
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join('uploads/recipe/', filename)



class UserManager(BaseUserManager):
    def create_user(self, email,password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have a valid email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = md.EmailField(max_length=255, unique=True)
    name = md.CharField(max_length=255)
    is_active = md.BooleanField(default=True)
    is_staff = md.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(md.Model):
    """ Tag to be used for a recipe"""

    name = md.CharField(max_length=255)
    user = md.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=md.CASCADE,
    )
    def __str__(self):
        return self.name

class Ingredient(md.Model):
    """Ingredient to be used in a recipe"""
    name = md.CharField(max_length=255)
    user = md.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=md.CASCADE
    )
    def __str__(self):
        return self.name


class Recipe(md.Model):
    """Recipe to be used"""
    title = md.CharField(max_length=255)
    user = md.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=md.CASCADE
    )
    price = md.DecimalField(max_digits=5, decimal_places=2)
    time_minutes = md.IntegerField()
    link = md.CharField(max_length=255, blank=True)
    ingredients = md.ManyToManyField('Ingredient')
    tags = md.ManyToManyField('Tag')
    image = md.ImageField(null=True, upload_to=recipe_image_file_path)
    def __str__(self):
        return self.title
