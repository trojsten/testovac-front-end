from django.shortcuts import render, get_object_or_404

from testovac.achievements.models import Achievement

def overview(request):
    achievements = Achievement.objects.all()
    context = locals()
    return render(request, "achievements/overview.html", context)

def detail(request, slug):
    achievement = get_object_or_404(Achievement, slug=slug)
    users = achievement.user.all()
    
    context = locals()
    return render(request, "achievements/detail.html", context)
