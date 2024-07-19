import re

from django import template
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wiki.models import URLPath

register = template.Library()


def static_menu_items(request):
    items = [
        # {
        #     "url_regex": r"^/news",
        #     "text": _("News"),
        #     "link": reverse("news_list", kwargs={"page": 1}),
        # },
        {
            "url_regex": r"^/tasks",
            "text": _("Tasks"),
            "link": reverse("contest_list"),
        },
        {
            "url_regex": r"^/results",
            "text": _("Results"),
            "link": "%s" % reverse("results_index"),
        },
        {
            "url_regex": r"^/achievements",
            "text": _("Achievements"),
            "link": reverse("achievement_overview"),
        },
    ]

    return items


def wiki_articles_in_menu(request):
    wiki_root = URLPath.root()

    urls = [wiki_root]
    for subroot in wiki_root.children.all():
        urls.append(subroot)

    items = []

    for url in urls:
        if url.article.can_read(request.user):
            items.append(
                {
                    "url_regex": r"^" + str(url) + ("$" if url.parent is None else ""),
                    "text": url.article.current_revision.title,
                    "link": url.article.get_absolute_url(),
                }
            )

    return items


@register.inclusion_tag("menu/menu.html", takes_context=True)
def menu(context):
    request = context.get("request")
    items = static_menu_items(request) + wiki_articles_in_menu(request)
    for item in items:
        item["is_active"] = bool(re.search(item["url_regex"], request.path))

    if request.user.is_staff:
        items.append(
            {
                "url_regex": r"^/admin",
                "text": "Admin",
                "link": reverse("admin:index"),
            }
        )

    return {"items": items}
