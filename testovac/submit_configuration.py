# When the submit app gets its own repository, these definitions will be moved to testovac/submit/
from collections import defaultdict

from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from testovac.results.generator import ResultsGenerator, display_points
from testovac.submit.defaults import submit_receiver_type
from testovac.submit.models import Submit
from testovac.submit.views import PostSubmitForm


class PostSubmitFormCustomized(PostSubmitForm):
    def is_submit_accepted(self, submit):
        """
        Submits after the contest has finished are automatically set to `not accepted`.
        Submit.is_accepted can be modified manually however.
        """

        if not submit.receiver.task:
            return Submit.NOT_ACCEPTED
        # TODO pari do pocitania vysledkovky
        # if task.contest.has_finished():
        # return Submit.NOT_ACCEPTED
        # else:
        return Submit.ACCEPTED

    def get_success_message(self, submit):
        message = super(PostSubmitFormCustomized, self).get_success_message(submit)
        if submit.is_accepted == Submit.ACCEPTED:
            return message
        else:
            return format_html(
                "{message}<br />{comment}",
                message=message,
                comment=_(
                    "Contest has already finished, this submit won't affect the results."
                ),
            )


def can_post_submit(receiver, user):
    task = receiver.task
    if not task:
        return False
    for contest in task.contests.all():
        if contest.tasks_visible_for_user(user):
            return True
    return False


def display_submit_receiver_name(receiver):
    type = submit_receiver_type(receiver)

    task = receiver.task
    if not task:
        return "no-task {} ({})".format(receiver.id, type)
    return "{} ({})".format(task.slug, type)


def display_score(review):
    task = review.submit.receiver.task
    if not task:
        return 0

    scores = defaultdict(lambda: None)
    scores[review.submit.receiver.pk] = review.score

    return display_points(ResultsGenerator.score_to_points(scores, task))


def default_inputs_folder_at_judge(receiver):
    if not receiver.task:
        return "{}-{}".format(settings.JUDGE_INTERFACE_IDENTITY, receiver.id)
    return receiver.task.slug
