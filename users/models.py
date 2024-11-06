from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver


# Create your models here.

@receiver(post_save, sender=User)
def add_user_to_student_group(sender, instance, created, **kwargs):
    if created:
        student_group, created = Group.objects.get_or_create(name='STUDENT')
        instance.groups.add(student_group)
