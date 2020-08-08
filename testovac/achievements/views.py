from django.shortcuts import get_object_or_404, render

from testovac.achievements.models import Achievement


def overview(request):
    return render(
        request,
        "achievements/overview.html",
        dict(achievements=Achievement.objects.all()),
    )


def detail(request, slug):
    achievement = get_object_or_404(Achievement, slug=slug)
    return render(
        request,
        "achievements/detail.html",
        dict(achievement=achievement, users=achievement.user.all()),
    )
