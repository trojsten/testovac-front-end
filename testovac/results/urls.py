from django.urls import re_path

from testovac.results.views import contest_results, results_index

urlpatterns = [
    re_path(r"^$", results_index, name="results_index"),
    re_path(
        r"^contest/(?P<contest_slug>[\w-]+)/$", contest_results, name="contest_results"
    ),
    re_path(r"^(?P<group>\w+)/$", results_index, name="results_index_group"),
    re_path(
        r"^contest/(?P<contest_slug>[\w-]+)/(?P<group>\w+)/$",
        contest_results,
        name="contest_results_group",
    ),
]
