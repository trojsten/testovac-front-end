from django.urls import re_path

from testovac.tasks.views import contest_list, task_statement, task_statement_download

urlpatterns = [
    re_path(r"^$", contest_list, name="contest_list"),
    re_path(r"^(?P<task_slug>[\w-]+)/$", task_statement, name="task_statement"),
    re_path(
        r"^(?P<task_slug>[\w-]+)/download/$",
        task_statement_download,
        name="task_statement_download",
    ),
]
