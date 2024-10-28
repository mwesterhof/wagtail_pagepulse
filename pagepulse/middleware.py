from threading import local

from wagtail.models import Page, Site

from .models import SeoStats

_locals = local()


def get_request():
    return getattr(_locals, 'request', None)


class PageTrackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _locals.request = request
        response = self.get_response(request)
        self._track_page(request, response)
        return response

    def _get_hostname(self, url):
        return url.split('//')[1].split('/')[0]

    def _track_page(self, request, response):
        context = getattr(response, 'context_data', None) or {}
        page = context.get('page')

        if not page:
            return

        if referer := request.headers.get('Referer'):
            page_hostname = self._get_hostname(page.full_url)
            referer_hostname = self._get_hostname(referer)

            if page_hostname != referer_hostname:
                seo_stats = SeoStats.objects.get(page=page)
                seo_stats.backlink_count += 1
                seo_stats.save()

