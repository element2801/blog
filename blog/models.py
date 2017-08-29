from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import *


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(User, blank=True, related_name='sub_bloggers')

    def __str__(self):
        return '{}'.format(self.user)


class Hidden(models.Model):
    class Meta:
        unique_together = ('user', 'post')
    user = models.ForeignKey(User)
    post = models.ForeignKey('Post')

    def __str__(self):
        return '{} {}'.format(self.user, self.post)


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=150)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.created)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
