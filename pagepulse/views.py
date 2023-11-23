from django.db.models import F
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from wagtail.admin.views.generic import WagtailAdminTemplateMixin
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page

from .models import get_scores_for_page, SeoStats


class SeoReportView(PageReportView):
    header_icon = 'crosshairs'
    template_name = "pagepulse/reports/seo_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("SEO report")
        return context

    def get_queryset(self):
        order = self.request.GET.get('order')

        qs = Page.objects.select_related('seo_stats').annotate(
            draft_score=F('seo_stats__draft_score'),
            live_score=F('seo_stats__live_score'),
            backlink_count=F('seo_stats__backlink_count'),
        ).filter(seo_stats__isnull=False)

        if order == 'live':
            return qs.order_by('live_score')
        if order == 'draft':
            return qs.order_by('draft_score')

        return qs

    list_export = [
        'title',
        'status_string',
        'url',
        'draft_score',
        'live_score',
        'backlink_count',
    ]

class SeoStatsView(WagtailAdminTemplateMixin, DetailView):
    template_name = "pagepulse/seo_stats.html"
    page_title = _("Dashboard")
    model = SeoStats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = self.get_object()

        context['scores'] = get_scores_for_page(stats.page)
        return context
