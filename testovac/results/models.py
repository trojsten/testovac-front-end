from django.db import models
from django.utils.translation import gettext_lazy as _
from sortedm2m.fields import SortedManyToManyField

from testovac.tasks.models import Contest


class CustomResultsTable(models.Model):
    slug = models.SlugField(
        primary_key=True,
        help_text="Serves as part of URL.<br />"
        'Must only contain characters "a-zA-Z0-9_-".',
    )
    name = models.CharField(max_length=128)
    number = models.IntegerField()
    contests = SortedManyToManyField(Contest)
    honor_contest_timeranges = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("custom results table")
        verbose_name_plural = _("custom results tables")

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)

    def task_list(self, user):
        tasks = []
        for contest in self.contests.all():
            if contest.tasks_visible_for_user(user):
                for task in contest.task_set.all():
                    task.start_time = (
                        contest.start_time
                        if self.honor_contest_timeranges
                        else self.start_time
                    )
                    task.end_time = (
                        contest.end_time
                        if self.honor_contest_timeranges
                        else self.end_time
                    )
                    tasks.append(task)
        return tasks
