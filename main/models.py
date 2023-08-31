from django.db import models
from django.contrib.auth.models import User
from django.db.models import Subquery
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=255, blank=True, null=False, default='main/default_avatar.jpg')
    experience = models.IntegerField(blank=True, null=False, default=0)
    levels = models.IntegerField(blank=True, null=False, default=0)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def get_friends(self):
        return self.friends.all()

    def get_not_friends(self):
        return Profile.objects.all().exclude(user__in=self.friends.all()).exclude(user=self.user)
    def __str__(self):
        return self.user.username
    def get_challenges(self):
        return UserChallenge.objects.filter(participant=self.user)
class Relationship(models.Model):
    STATUS_CHOICES = [
        ('send', 'send'),
        ('accepted', 'accepted'),
    ]
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
class Challenge(models.Model):
    COLOR_CHOICES = [
        ('#ffbe0b', 'Amber'),
        ('#fb5607', 'Orange Pantone'),
        ('#FF006E', 'Winter Sky'),
        ('#8338EC', 'Blue Violet'),
        ('#3A86FF', 'Azure'),
    ]
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_creator')
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    hours = models.IntegerField(blank=False, null=False, default=1)
    participants = models.ManyToManyField(User, through='UserChallenge', related_name='user_participant')
    reward = models.IntegerField(blank=False,null=False, default=0)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=False, default='#3A86FF')

    def get_all_self_hours(self):
        return UserChallenge.objects.filter(challenge=self)
    def __str__(self):
        return self.title

class ChallengeRelationship(models.Model):
    STATUS_CHOICES = [
        ('send', 'send'),
        ('accepted', 'accepted'),
    ]
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='challenge_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='challenge_receiver')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='relation_challenge')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver', 'challenge', )

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.challenge}-{self.status}"

class UserChallenge(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    self_hours = models.IntegerField(null=False, default=0)
    is_finished = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.participant.username + " : " + self.challenge.title

class Task(models.Model):
    TYPE_CHOICES = [
        (1, 'ONEDAY'),
        (2, 'ROUTINE'),
        (3, 'CHALLENGETASK'),
        (4, 'LONGTIME'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    is_finished = models.BooleanField(null=False, default=False)
    type = models.IntegerField(null=False, blank=False, choices=TYPE_CHOICES, default=1)
    def __str__(self):
        return self.user.username + " : " + self.title + " : " + self.get_type_display()
