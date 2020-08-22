from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.module_loading import import_string

from testovac.results.generator import ResultsGenerator
from testovac.tasks.models import Competition, Task
from testovac.utils import is_true


def contest_list(request):
    visible_contests = Competition.objects.get(
        pk=settings.CURRENT_COMPETITION_PK
    ).get_visible_contests(request.user)
    visible_contests = visible_contests.prefetch_related("task_set__submit_receivers")

    receiver_lists_as_strings = []
    for contest in visible_contests:
        receivers = []
        for task in contest.task_set.all():
            for receiver in task.submit_receivers.all():
                receivers.append(receiver.pk)
        receivers_string = ",".join(map(str, receivers))
        receiver_lists_as_strings.append(receivers_string)

    user_task_points = ResultsGenerator(
        User.objects.filter(pk=request.user.pk),
        Task.objects.filter(contests__in=visible_contests),
    ).get_user_task_points()

    completed_tasks = []
    completed_contests = []
    hide_finished = is_true(request.GET.get("hide_finished", False))
    if hide_finished:
        for task in Task.objects.filter(contests__in=visible_contests):
            if user_task_points[request.user.pk][task.pk] == task.max_points:
                completed_tasks.append(task)

        for contest in visible_contests:
            completed = True
            for task in contest.task_set.all():
                if task not in completed_tasks:
                    completed = False
            if completed:
                completed_contests.append(contest)

    template_data = {
        "contests_with_receivers": zip(visible_contests, receiver_lists_as_strings),
        "user_task_points": user_task_points,
        "completed_tasks": completed_tasks,
        "completed_contests": completed_contests,
        "hide_finished": hide_finished,
    }

    return render(request, "tasks/contest_list.html", template_data,)


def task_statement(request, task_slug):
    task = get_object_or_404(Task, pk=task_slug)
    is_visible = False
    for contest in task.contests.all():
        if contest.tasks_visible_for_user(request.user):
            is_visible = True
    if not is_visible:
        raise Http404

    user_task_points = ResultsGenerator(
        User.objects.filter(pk=request.user.pk), (task,)
    ).get_user_task_points()

    template_data = {
        "task": task,
        "user_task_points": user_task_points,
        "user_points": user_task_points[request.user.pk][task.pk] or 0,
        "statement": import_string(settings.TASK_STATEMENTS_BACKEND)().render_statement(
            request, task
        ),
    }
    return render(request, "tasks/task_statement.html", template_data,)


def task_statement_download(request, task_slug):
    task = get_object_or_404(Task, pk=task_slug)
    is_visible = False
    for contest in task.contests.all():
        if contest.tasks_visible_for_user(request.user):
            is_visible = True
    if not is_visible:
        raise Http404
    return import_string(settings.TASK_STATEMENTS_BACKEND)().download_statement(
        request, task
    )
