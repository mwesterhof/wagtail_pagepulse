from django.contrib import messages
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from wagtail.models import Page, Revision
from wagtail.signals import page_published

from .models import SeoStats

from .middleware import get_request


@receiver(post_save, sender=Revision)
def update_draft_stats(sender, instance, **kwargs):
    if not issubclass(instance.content_type.model_class(), Page):
        return

    page = instance.content_object
    stats, _ = SeoStats.objects.get_or_create(page=page)
    stats.update_draft_stats(instance)
    messages.info(get_request(), f"Draft updated, SEO score: {stats.draft_score}")


@receiver(page_published)
def update_live_stats(sender, instance, **kwargs):
    stats, _ = SeoStats.objects.get_or_create(page=instance)
    stats.update_live_stats()
    messages.info(get_request(), f"Page published, SEO score: {stats.live_score}")
