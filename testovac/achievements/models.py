from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField

from testovac.submit.models import Review
from testovac.tasks.models import Task


class Achievement(models.Model):
    slug = models.SlugField(
        primary_key=True,
        help_text="Must be unique among all achievements, serves as part of URL.<br />"
        'Must only contain characters "a-zA-Z0-9_-".',
    )
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    users = models.ManyToManyField(
        User, related_name="achievements", through="AchievementToUser"
    )

    def get_absolute_url(self):
        return reverse("achievement_detail", kwargs={"slug": self.slug})


class AchievementTaskSet(models.Model):
    """
    One Achievement is related to set of tasks.
    """

    slug = models.SlugField(
        primary_key=True,
        help_text="Must be unique among all achievement task sets, serves as part of URL.<br />"
        'Must only contain characters "a-zA-Z0-9_-".',
    )
    name = models.CharField(max_length=128)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    tasks = SortedManyToManyField(Task)

    @receiver(post_save, sender=Review, weak=False)
    def handler(sender, **kwargs):
        review = kwargs["instance"]
        user = review.submit.user
        task = review.submit.receiver.task
        for achievementTaskSet in AchievementTaskSet.objects.filter(tasks__in=[task]):
            task_list = achievementTaskSet.tasks.all()
            if (
                Review.objects.order_by("submit", "-time")
                .distinct("submit")
                .filter(
                    score=100,
                    submit__user=user,
                    submit__receiver__task__in=task_list,
                )
                .values("submit__receiver__task")
                .distinct()
                .count()
                == len(task_list)
                and AchievementToUser.objects.filter(
                    achievement=achievementTaskSet.achievement, user=user
                ).count()
                == 0
            ):
                achievementToUser = AchievementToUser(
                    achievement=achievementTaskSet.achievement, user=user
                )
                achievementToUser.save()
                # achievementTaskSet.achievement.users.add(user)


class AchievementToUser(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField(default=datetime.now)
