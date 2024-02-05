import os

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile

from testovac.submit import constants
from testovac.submit import settings as submit_settings
from testovac.submit.submit_helpers import add_language_preference_to_filename


class FileSubmitForm(forms.Form):
    """
    Reusable form for file uploading.
    Constructor takes additional keyword argument 'configuration' - a dict with parameters.
    """

    def __init__(self, *args, **kwargs):
        config = kwargs.pop("configuration")
        super(FileSubmitForm, self).__init__(*args, **kwargs)

        self.extensions = config.get("extensions", None)
        self.languages = config.get("languages", None)

        if self.languages is not None:
            automatic = [
                [
                    constants.DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION,
                    constants.DEDUCE_LANGUAGE_AUTOMATICALLY_VERBOSE,
                ]
            ]
            self.fields["language"] = forms.ChoiceField(
                initial='.py', label=_("Language"), choices=automatic + self.languages, required=True, widget=forms.HiddenInput()
            )

    submit_file = forms.FileField(
        max_length=submit_settings.SUBMIT_UPLOADED_FILENAME_MAXLENGTH,
        allow_empty_file=True,
        required=False,
        widget=forms.HiddenInput()
    )

    python_code = forms.CharField(
        widget=forms.Textarea, label=_("Python Code"), required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        python_code = cleaned_data.get('python_code')
        cleaned_data['submit_file'] = ContentFile(python_code.encode('utf-8'))
        cleaned_data['submit_file'].name = 'submit.py'