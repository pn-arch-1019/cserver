from django.contrib.sitemaps import Sitemap 
from django.urls import reverse 


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8 


    def item(self):
        return ['index']
    

    def location(self, item):
        return reverse(item)
