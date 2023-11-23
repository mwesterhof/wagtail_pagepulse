from django.contrib import admin

from .models import SeoStats


class SeoStatsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'live_score', 'draft_score', 'backlink_count')


admin.site.register(SeoStats, SeoStatsAdmin)
