from django.db import models
from django.conf import settings
from wagtail.models import Page

seo_config = getattr(settings, 'PAGEPULSE_CONFIG', {})


# TODO: pick actual values
MIN_TITLE_LENGTH = seo_config.get('MIN_TITLE_LENGTH', 10)
MAX_TITLE_LENGTH = seo_config.get('MAX_TITLE_LENGTH', 100)
MIN_DESCRIPTION_LENGTH = seo_config.get('MIN_DESCRIPTION_LENGTH', 20)
MAX_DESCRIPTION_LENGTH = seo_config.get('MAX_DESCRIPTION_LENGTH', 200)
MIN_TITLE_WORD_COUNT = seo_config.get('MIN_TITLE_WORD_COUNT', 2)
MAX_TITLE_WORD_COUNT = seo_config.get('MAX_TITLE_WORD_COUNT', 10)


class ScoreReport:
    def __init__(self):
        self.success_messages = []
        self.fail_messages = []
        self.total_score = 0

    def success(self, message, points):
        self.total_score += points
        self.success_messages.append(
            f"{message}: {points}"
        )

    def fail(self, message, points):
        self.fail_messages.append(
            f"{message}: {points}"
        )


def _calculate_score(title, search_description):
    report = ScoreReport()

    title_length = len(title)
    title_word_count = len(title.split())
    description_length = len(search_description)

    if MIN_TITLE_LENGTH <= title_length <= MAX_TITLE_LENGTH:
        report.success(f"Title length is between {MIN_TITLE_LENGTH} and {MAX_TITLE_LENGTH} ({title_length})", 30)
    else:
        report.fail(f"Title length should be between {MIN_TITLE_LENGTH} and {MAX_TITLE_LENGTH} (is {title_length})", 30)
        
    if MIN_TITLE_WORD_COUNT <= title_word_count <= MAX_TITLE_WORD_COUNT:
        report.success(f"Title word count is between {MIN_TITLE_WORD_COUNT} and {MAX_TITLE_WORD_COUNT} ({title_word_count})", 30)
    else:
        report.fail(f"Title word count should be between {MIN_TITLE_WORD_COUNT} and {MAX_TITLE_WORD_COUNT} (is {title_word_count})", 30)

    if MIN_DESCRIPTION_LENGTH <= description_length <= MAX_DESCRIPTION_LENGTH:
        report.success(f"Description length is between {MIN_DESCRIPTION_LENGTH} and {MAX_DESCRIPTION_LENGTH} ({description_length})", 30)
    else:
        report.fail(f"Description length should be between {MIN_DESCRIPTION_LENGTH} and {MAX_DESCRIPTION_LENGTH} (is {description_length})", 30)
        
    return report


def get_scores_for_page(page):
    revision = page.revisions.order_by('-created_at').first()

    live_score = _calculate_score(page.title, page.search_description)
    draft_score = _calculate_score(
        revision.content['title'],
        revision.content['search_description']
    )

    return {
        'live': live_score,
        'draft': draft_score
    }


def _get_live_page_score(page):
    import ipdb; ipdb.set_trace() 
    report = _calculate_score(page.title, page.search_description)
    return report.total_score


def _get_draft_page_score(revision):
    import ipdb; ipdb.set_trace() 
    title = revision.content['title']
    search_description = revision.content['search_description']

    report = _calculate_score(title, search_description)
    return report.total_score


class SeoStats(models.Model):
    page = models.OneToOneField(Page, related_name='seo_stats', on_delete=models.CASCADE)
    live_score = models.PositiveSmallIntegerField(default=0)
    draft_score = models.PositiveSmallIntegerField(default=0)
    backlink_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.page}"

    class Meta:
        verbose_name_plural = "Page stats"

    def update_draft_stats(self, revision):
        self.draft_score = _get_draft_page_score(revision)
        self.save()

    def update_live_stats(self):
        self.live_score = _get_live_page_score(self.page)
        self.save()
