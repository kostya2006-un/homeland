from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Profile

@receiver(user_signed_up)
def create_profile(sender, request, user, **kwargs):
    Profile.objects.create(user=user)