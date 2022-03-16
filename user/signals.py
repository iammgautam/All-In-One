from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile
from django.contrib.auth.models import User


# this signal will create a profile for a new user with name,email,username instance
@receiver(post_save, sender=User)
def create_profile_user(sender, instance, created, *args, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            username=user.username,
            f_name=user.first_name,
            l_name=user.last_name,
            email=user.email,
        )


# this signal will save the profile instance from a new user creation
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, created, **kwargs):
#     instance.profile.save()

# this signal will update the user's name,email,username, if updated through profile form by user.


@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, *args, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.f_name
        user.last_name = profile.l_name
        user.username = profile.username
        user.email = profile.email
        user.save()

# this signal will delete the user account if deleted through profile by user itself.


@receiver(post_delete, sender=Profile)
def UserDelete(sender, instance, *args, **kwargs):
    user = instance.user
    user.delete()
