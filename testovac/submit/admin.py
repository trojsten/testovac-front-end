from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from zipfile import ZipFile
import io

from testovac.submit.models import (
    Review,
    Submit,
    SubmitReceiver,
    SubmitReceiverTemplate,
)
from testovac.tasks.models import Task


class SubmitReceiverTemplateAdmin(admin.ModelAdmin):
    pass


class LoadConfigurationFromTemplate(forms.Select):
    class Media:
        js = ("submit/load-configuration-from-template.js",)


#class SubmitReceiverForm(forms.ModelForm):
#    receiver_template = forms.ChoiceField(
#        choices=((x.id, str(x)) for x in SubmitReceiverTemplate.objects.all()),
#        widget=LoadConfigurationFromTemplate(),
#    )

#    class Meta:
#        model = SubmitReceiver
#        fields = ("receiver_template", "configuration", "task")
#        widgets = {"configuration": forms.Textarea(attrs={"rows": 15, "cols": 40})}


class SubmitReceiverAdmin(admin.ModelAdmin):
    pass


class ReviewInline(admin.StackedInline):
    model = Review
    fields = ("time", "score", "short_response", "comment", "filename")
    readonly_fields = ("time",)
    ordering = ("-time",)
    extra = 0


class ViewOnSiteMixin(object):
    def view_on_site_list_display(self, obj):
        return mark_safe(
            u'<a href="{}">{}</a>'.format(obj.get_absolute_url(), "view on site")
        )

    view_on_site_list_display.allow_tags = True
    view_on_site_list_display.short_description = u"View on site"

def export_as_zip(modeladmin, request, queryset):
    zipfile = io.BytesIO()
    with ZipFile(zipfile,'w') as zf:
        for submit in queryset:
            zf.write(submit.file_path(), arcname='{}_{}_{}'.format(submit.id, submit.user.get_full_name(), submit.filename))
    zipfile.seek(0)
    return HttpResponse(zipfile, content_type="application/zip")

class SubmitAdmin(ViewOnSiteMixin, admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = (
        "submit_id",
        "view_on_site_list_display",
        "receiver",
        "user",
        "status",
        "score",
        "time",
        "is_accepted",
        "is_public",
        "filename",
    )
    search_fields = ("user__username", "user__first_name", "user__last_name")
    actions = [export_as_zip]
    list_max_show_all = 2000

    def submit_id(self, submit):
        return "submit %d" % (submit.id,)

    def status(self, submit):
        review = submit.last_review()
        return review.short_response if review is not None else ""

    def score(self, submit):
        review = submit.last_review()
        return review.display_score() if review is not None else ""

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(SubmitAdmin, self).get_search_results(
            request, queryset, search_term
        )
        try:
            search_term_as_receiver_ids = Task.objects.filter(
                slug__icontains=search_term
            ).values_list("submit_receivers__id", flat=True)
            queryset |= self.model.objects.filter(
                receiver_id__in=search_term_as_receiver_ids
            )
        except:
            pass
        return queryset, use_distinct


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(SubmitReceiverTemplate, SubmitReceiverTemplateAdmin)
admin.site.register(SubmitReceiver, SubmitReceiverAdmin)
admin.site.register(Submit, SubmitAdmin)
admin.site.register(Review, ReviewAdmin)
