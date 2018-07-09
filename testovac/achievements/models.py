from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

from sortedm2m.fields import SortedManyToManyField

from testovac.tasks.models import Task
from testovac.submit.models import Review

from datetime import datetime

class Achievement(models.Model):
    slug = models.SlugField(primary_key=True,
                            help_text='Must be unique among all achievements, serves as part of URL.<br />'
                                      'Must only contain characters "a-zA-Z0-9_-".')
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    user = models.ManyToManyField(User, related_name="achievements", through='AchievementToUser')

    def get_absolute_url(self):
        return reverse('achievement_detail', kwargs={'slug': self.slug})

    def award_to(self, user):
        if not self in user.achievements.all():
            AchievementToUser.objects.create(achievement=self, user=user)


class AchievementTaskSet(models.Model):
    """
    One Achievement is related to set of tasks.
    """
    slug = models.SlugField(primary_key=True,
                            help_text='Must be unique among all achievement task sets, serves as part of URL.<br />'
                                      'Must only contain characters "a-zA-Z0-9_-".')
    name = models.CharField(max_length=128)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    tasks = SortedManyToManyField(Task)


    @receiver(post_save, sender=Review, weak=False)
    def handler(sender, **kwargs):
        review = kwargs['instance']
        user = review.submit.user
        for achievementTaskSet in AchievementTaskSet.objects.all():
            task_list = achievementTaskSet.tasks.all()
            solved_all = True
            for task in task_list:
                if not Review.objects.filter(submit__user=user,
                                        submit__receiver__in=task.submit_receivers.all(), 
                                        score=100).exists():
                    solved_all = False

            if solved_all:
                achievement = Achievement.objects.get(slug=achievementTaskSet.slug)
                print("AWARDINGGGGGGGGGGGGGGGGGGGGGGGGGGG")
                achievement.award_to(user)


class AchievementToUser(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField(default=datetime.now)
