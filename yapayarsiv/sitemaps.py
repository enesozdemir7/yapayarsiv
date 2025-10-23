from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from forum.models import News, Tool
from tools.models import ToolCategories2, ToolSubCategories

class StaticPagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return ["forum:all_posts", "forum:all_news", "forum:contact", "forum:forum", "user:register", "user:login"]

    def location(self, item):
        return reverse(item)

class ToolSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Tool.objects.filter(visible=True)

    def location(self, obj: Tool) -> str:
        return obj.get_absolute_url()

class ToolCategorySiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ToolCategories2.objects.all()

    def location(self, obj: ToolCategories2) -> str:
        return obj.get_absolute_url()

class ToolSubCategorySiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ToolSubCategories.objects.all()

    def location(self, obj: ToolSubCategories) -> str:
        return obj.get_absolute_url()

class NewsSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return News.objects.filter(visible=True)

    def location(self, obj: News) -> str:
        return obj.get_absolute_url()
