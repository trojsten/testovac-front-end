from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from testovac.achievements.models import Achievement, AchievementTaskSet

from testovac.submit.models import Review
from testovac.tasks.models import Task


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'description')

class AchievementTaskSetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    exclude = ('achievement', )

    def save_model(self, request, obj, form, change):

        self.slug=obj.slug
        #TODO if change, update achievement
        if not change:
            obj.achievement = Achievement.objects.create(
                                slug=obj.slug,
                                name=obj.name,
                                description=""
                              )
        super(AchievementTaskSetAdmin,self).save_model(request, obj, form, change)


    def save_related(self, request, form, formsets, change):
        super(AchievementTaskSetAdmin,self).save_related(request, form, formsets, change)
        achievement = Achievement.objects.get(slug=self.slug)
        task_list = AchievementTaskSet.objects.get(slug=self.slug).tasks.all()
        for task in task_list:
            achievement.description+=task.name+", "
        achievement.description=achievement.description[:-2]
        achievement.save()
        for user in User.objects.all():
            solved_all = True
            for task in task_list:
                if not Review.objects.filter(submit__user=user,
                                        submit__receiver__in=task.submit_receivers.all(),
                                        score=100).exists():
                    solved_all = False

            if solved_all:
                achievement.award_to(user)

admin.site.register(AchievementTaskSet, AchievementTaskSetAdmin)
admin.site.register(Achievement, AchievementAdmin)
