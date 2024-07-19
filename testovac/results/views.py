from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from testovac.results.models import CustomResultsTable
from testovac.tasks.models import Competition, Contest


def results_index(request, group=None):
    custom_tables = CustomResultsTable.objects.order_by("number").prefetch_related(
        "contests__task_set"
    )
    custom_tables_data = []
    for custom_table in custom_tables:
        custom_tables_data.append(
            {
                "custom_table": custom_table,
                "task_list": custom_table.task_list(request.user),
            }
        )

    contests = (
        Competition.objects.get(pk=settings.CURRENT_COMPETITION_PK)
        .contests.all()
        .prefetch_related("task_set")
    )
    visible_contests = [
        contest for contest in contests if contest.tasks_visible_for_user(request.user)
    ]

    return render(
        request,
        "results/results_index.html",
        {
            "custom_tables": custom_tables_data,
            "contests": visible_contests,
            "group": group,
        },
    )


def contest_results(request, contest_slug, group=None):
    contest = get_object_or_404(Contest, pk=contest_slug)
    if not contest.tasks_visible_for_user(request.user):
        raise Http404

    tasks = list(contest.task_set.all())
    for task in tasks:
        task.start_time = contest.start_time
        task.end_time = contest.end_time

    return render(
        request,
        "results/contest_results_table.html",
        {
            "contest": contest,
            "task_list": tasks,
            "group": group,
        },
    )
