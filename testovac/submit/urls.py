from django.urls import re_path
from django.utils.module_loading import import_string

from . import settings as submit_settings
from .commands import rejudge_receiver_submits, rejudge_submit
from .views import (
    download_review,
    download_submit,
    get_receiver_templates,
    receive_protocol,
    view_submit,
)

urlpatterns = [
    re_path(
        r"^post/(?P<receiver_id>\d+)/$",
        import_string(submit_settings.SUBMIT_POST_SUBMIT_FORM_VIEW).as_view(),
        name="post_submit",
    ),
    re_path(r"^view/(?P<submit_id>\d+)/$", view_submit, name="view_submit"),
    re_path(
        r"^download/submit/(?P<submit_id>\d+)/$",
        download_submit,
        name="download_submit",
    ),
    re_path(
        r"^download/review/(?P<review_id>\d+)/$",
        download_review,
        name="download_review",
    ),
    re_path(r"^receive_protocol/$", receive_protocol),
    re_path(
        r"^commands/rejudge/submit/(?P<submit_id>\d+)/$",
        rejudge_submit,
        name="rejudge_submit",
    ),
    # This the url path for this command is currently deactivated.
    # Also the button at submit_list template is hidden to prevent misclicks that could cause a judge overflow.
    # TODO: Implement pop-up / confirmation page for resubmit approval
    re_path(
        r"^commands/rejudge/receiver/(?P<receiver_id>\d+)/$",
        rejudge_receiver_submits,
        name="rejudge_receiver_submits",
    ),
    re_path(r"^ajax/get_receiver_templates/", get_receiver_templates),
]
