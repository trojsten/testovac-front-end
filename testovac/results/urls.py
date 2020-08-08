from django.conf.urls import url

from testovac.results.views import contest_results, results_index

urlpatterns = [
    url(r"^$", results_index, name="results_index"),
    url(
        r"^contest/(?P<contest_slug>[\w-]+)/$", contest_results, name="contest_results"
    ),
    url(r"^(?P<group>\w+)/$", results_index, name="results_index_group"),
    url(
        r"^contest/(?P<contest_slug>[\w-]+)/(?P<group>\w+)/$",
        contest_results,
        name="contest_results_group",
    ),
]
