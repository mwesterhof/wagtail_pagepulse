from django.urls import path, reverse

from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail import hooks

from .views import SeoStatsView, SeoReportView


@hooks.register('register_reports_menu_item')
def register_seo_report():
    return AdminOnlyMenuItem("Seo Report", reverse('seo-report'), icon_name=SeoReportView.header_icon, order=700)


@hooks.register('register_admin_urls')
def register_seo_report_url():
    return [
        path('reports/seo/', SeoReportView.as_view(), name='seo-report'),
        path('reports/seo/<int:pk>/', SeoStatsView.as_view(), name='seo-stats'),
    ]
