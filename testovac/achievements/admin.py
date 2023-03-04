from django.contrib import admin
from django.contrib.auth.models import User

from testovac.achievements.models import Achievement, AchievementTaskSet, AchievementToUser


class AchievementAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "description")


class AchievementTaskSetAdmin(admin.ModelAdmin):
    list_display = ("slug", "name")
    exclude = ("achievement",)

    def save_model(self, request, obj, form, change):

        self.slug = obj.slug
        if not change:
            obj.achievement = Achievement.objects.create(
                slug=obj.slug, name=obj.name, description=""
            )
        super(AchievementTaskSetAdmin, self).save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super(AchievementTaskSetAdmin, self).save_related(
            request, form, formsets, change
        )
        achievement = form.instance.achievement
        task_list = AchievementTaskSet.objects.get(slug=self.slug).tasks.all()
        achievement.name = form.instance.name
        achievement.description = ", ".join(task.name for task in task_list)
        achievement.save()
        task_list = [t.pk for t in task_list]
        for user in User.objects.raw(
            """
SELECT "auth_user"."id"
FROM "auth_user"
WHERE (
    SELECT COUNT(DISTINCT V1."task_id")
    FROM "submit_submit" V0
    INNER JOIN "submit_submitreceiver" V1 ON (V0."receiver_id" = V1."id")
    WHERE (V1."task_id" = ANY(%s)
            AND V0."user_id" = "auth_user"."id"
            AND (
                SELECT U0."score"
                FROM "submit_review" U0
                WHERE U0."submit_id" = V0."id"
                ORDER BY U0."time" DESC LIMIT 1) = 100.0
            )
    ) = %s
""",
            [task_list, len(task_list)],
        ):
            achievement.users.add(user)

class AchievementToUserAdmin(admin.ModelAdmin):
    list_display = ("created", "user", "achievement")

admin.site.register(AchievementTaskSet, AchievementTaskSetAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchievementToUser, AchievementToUserAdmin)
