from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, re_path
from django.views.static import serve
from django_nyt.urls import get_pattern as get_nyt_pattern
from wiki.urls import get_pattern as get_wiki_pattern

import testovac.achievements.urls
import testovac.login.urls
import testovac.results.urls
import testovac.submit.urls
import testovac.tasks.urls
from testovac.admin import admin_site_custom_index_view


def create_custom_admin_urls(urls):
    def get_admin_urls():
        return [
            re_path(r"^$", admin.site.admin_view(admin_site_custom_index_view))
        ] + urls

    return get_admin_urls


admin.site.get_urls = create_custom_admin_urls(admin.site.get_urls())


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^tasks/", include(testovac.tasks.urls)),
    re_path(r"^submit/", include(testovac.submit.urls)),
    # re_path(r"^news/", include(news.urls)),
    re_path(r"^results/", include(testovac.results.urls)),
    re_path(r"^login/", include(testovac.login.urls)),
    re_path(r"^achievements/", include(testovac.achievements.urls)),
]

urlpatterns += [
    re_path(r"^notifications/", get_nyt_pattern()),
    re_path(r"^$", lambda r: HttpResponseRedirect("wiki/"), name="root"),
    re_path(r"^wiki/", get_wiki_pattern()),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
