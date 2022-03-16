from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


def profile_picture_path(instance, filename):
    return 'profile/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=200, verbose_name='First Name')
    l_name = models.CharField(max_length=200, verbose_name='Last Name')
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    profileImg = models.ImageField(null=True, blank=True,upload_to=profile_picture_path,default='default.png', verbose_name='Profile Picture')
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.username
