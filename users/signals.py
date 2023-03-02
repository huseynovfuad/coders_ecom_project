from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def my_handler(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )