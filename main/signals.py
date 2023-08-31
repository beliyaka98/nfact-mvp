from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship, ChallengeRelationship, UserChallenge

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

@receiver(post_save, sender=ChallengeRelationship)
def post_save_add_to_challenge(sender, created, instance, **kwargs):
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        instance.challenge.participants.add(receiver_.user)
