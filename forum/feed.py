from django.urls import reverse
from .models import News
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.timezone import now

class CustomFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement("image", item["image"])

class NewsFeed(Feed):
    feed_type = CustomFeed
    title = "Yapay Arşiv"
    link = "http://yapayarsiv.com"
    description = "Türkiye'nin Yapay Zeka Arşivi; Binlerce Yapay Zeka Aracı İçin Tek Platform!"

    def items(self):
        return News.objects.filter(visible=True)[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_pubdate(self, item):
        return item.created_at

    def item_link(self, item):
        return f"http://yapayarsiv.com{reverse('forum:news', args=[item.slug])}"

    def item_extra_kwargs(self, item):
        return {'image': f"http://yapayarsiv.com{item.banner.url}"}

    def link(self):
        return "http://yapayarsiv.com/feed/"
