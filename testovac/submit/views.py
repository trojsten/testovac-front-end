import os
from glob import glob

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from testovac.results.generator import ResultsGenerator

from testovac.tasks.models import Task

from testovac.submit.constants import JudgeTestResult, ReviewResponse
from testovac.submit.forms import FileSubmitForm
from testovac.submit.judge_helpers import (
    JudgeConnectionError,
    create_review_and_send_to_judge,
    parse_protocol,
)
from testovac.submit.models import Review, Submit, SubmitReceiver, SubmitReceiverTemplate
from testovac.submit.submit_helpers import create_submit, send_file, write_chunks_to_file


class PostSubmitForm(View):
    login_required = True

    def is_submit_accepted(self, submit):
        """
        Override this method to decide which submits will be accepted, penalized or not accepted.
        This method is called after the submit is created, but before it is saved in database.
        E.g. submits after deadline are not accepted.
        """
        return Submit.ACCEPTED

    def get_success_message(self, submit):
        """
        This message will be added to `messages` after successful submit.
        """
        if submit.receiver.configuration.get("send_to_judge", False):
            return format_html(
                _(
                    'Submit successful. Testing protocol will be soon available <a href="{link}">here</a>.'
                ),
                link=reverse("view_submit", args=[submit.id]),
            )
        return _("Submit successful.")

    def send_to_judge(self, submit):
        create_review_and_send_to_judge(submit)

    def post(self, request, receiver_id):
        receiver = get_object_or_404(SubmitReceiver, pk=receiver_id)
        config = receiver.configuration

        if not receiver.can_post_submit(request.user):
            raise PermissionDenied()

        if "form" in config:
            form = FileSubmitForm(request.POST, request.FILES, configuration=config["form"])
        else:
            raise PermissionDenied()

        if form.is_valid():
            submit = create_submit(
                user=request.user,
                receiver=receiver,
                is_accepted_method=self.is_submit_accepted,
                sfile=form.cleaned_data["submit_file"],
            )
        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR, "%s: %s" % (field.label, error))
            for error in form.non_field_errors():
                messages.add_message(request, messages.ERROR, error)
            return redirect(request.POST["redirect_to"])

        if config.get("send_to_judge", False):
            try:
                self.send_to_judge(submit)
            except JudgeConnectionError:
                messages.add_message(
                    request, messages.ERROR, _("Upload to judge was not successful.")
                )
                return redirect(request.POST["redirect_to"])

        messages.add_message(request, messages.SUCCESS, self.get_success_message(submit))
        return redirect(request.POST["redirect_to"])


@login_required
def view_submit(request, submit_id):
    submit = get_object_or_404(
        Submit.objects.select_related("receiver").select_related("receiver__task"),
        pk=submit_id,
    )
    user_has_admin_privileges = submit.receiver.has_admin_privileges(request.user)

    def get_submit_picture(is_positive, submit_id):
        if is_positive:
            dirn = "positive/"
        else:
            dirn = "negative/"
        files = [
            os.path.basename(x) for x in glob(os.path.join(settings.STATIC_ROOT, "gifs", dirn, "*"))
        ]
        if files == []:
            return None
        files.sort()

        picture_id = submit_id % len(files)
        return "/static/gifs/%s%s" % (dirn, files[picture_id])

    def get_image(review, max_points, submit_id):
        if review.short_response == "OK":
            return get_submit_picture(True, submit_id)
        if review.short_response == "Sent to judge":
            return None
        if review.score < max_points * 0.32:
            return get_submit_picture(False, submit_id)
        return None

    if submit.user != request.user and not user_has_admin_privileges and not submit.is_public:
        raise PermissionDenied()

    conf = submit.receiver.configuration
    task = submit.receiver.task
    review = submit.last_review()
    data = {
        "submit": submit,
        "task_id": str(submit.receiver).split()[0],
        "review": review,
        "image": get_image(review, task.max_points, int(submit_id)),
        "user_has_admin_privileges": user_has_admin_privileges,
        "show_submitted_file": conf.get("show_submitted_file", False),
        "protocol_expected": conf.get("send_to_judge", False),
    }

    if data["show_submitted_file"]:
        try:
            with open(
                submit.file_path(), "r", encoding="utf-8", errors="replace"
            ) as submitted_file:
                data["submitted_file"] = submitted_file.read()
        except FileNotFoundError:
            data["submitted_file"] = "NOT FOUND"

    if data["protocol_expected"] and review and review.protocol_exists():
        force_show_details = (
            conf.get("show_all_details", False)
            or user_has_admin_privileges
            or Task.objects.get(pk=str(submit.receiver).split()[0]).show_details
        )
        data["protocol"] = parse_protocol(review.protocol_path(), force_show_details)
        data["result"] = JudgeTestResult

    if submit.is_public and (request.GET.get("ref") is not None or submit.user != request.user):
        user_task_points = ResultsGenerator(
            User.objects.filter(pk=request.user.pk), (task,)
        ).get_user_task_points()
        if (user_task_points[request.user.pk][task.pk] or 0) + 1e-7 < task.max_points:
            raise PermissionDenied()
        return render(request, "submit/view_reference_submit.html", data)
    else:
        return render(request, "submit/view_submit.html", data)


@login_required
def download_submit(request, submit_id):
    submit = get_object_or_404(Submit.objects.select_related("receiver"), pk=submit_id)
    if submit.user != request.user and not submit.receiver.has_admin_privileges(request.user):
        raise PermissionDenied()
    return send_file(request, submit.file_path(), submit.filename)


@login_required
def download_review(request, review_id):
    review = get_object_or_404(
        Review.objects.select_related("submit", "submit__receiver"), pk=review_id
    )
    if review.submit.user != request.user and not review.submit.receiver.has_admin_privileges(
        request.user
    ):
        raise PermissionDenied()
    return send_file(request, review.file_path(), review.filename)


@csrf_exempt
@require_POST
def receive_protocol(request):
    """
    Receive protocol from judge via POST and save it to review.protocol_path()
    """
    review_id = request.POST["submit_id"]
    review = get_object_or_404(Review, pk=review_id)
    protocol = request.POST["protocol"].encode("utf-8")
    write_chunks_to_file(review.protocol_path(), [protocol])

    protocol_data = parse_protocol(review.protocol_path())
    if protocol_data["ready"]:
        review.score = protocol_data["score"]
        review.short_response = protocol_data["final_result"]
    else:
        review.short_response = ReviewResponse.PROTOCOL_CORRUPTED
    review.save()

    return HttpResponse("")


@login_required
def get_receiver_templates(request):
    """
    Send receiver templates to JavaScript at page admin:submit_submitreceiver_change/add
    """
    if not request.user.is_staff:
        raise PermissionDenied()
    templates = SubmitReceiverTemplate.objects.all()
    templates = {template.id: template.configuration for template in templates}
    return JsonResponse(templates)
