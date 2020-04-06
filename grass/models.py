from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from content_editor.models import Region, create_plugin_base, Template

from feincms3 import plugins
from feincms3.mixins import TemplateMixin
from feincms3_meta.models import MetaMixin

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=180)

    def __str__(self):
        return self.name


class Location(models.Model):
    zip_code = models.SmallIntegerField()

    city = models.CharField(max_length=120)

    lat = models.FloatField()
    lng = models.FloatField()


class Grassroot(models.Model):
    categories = models.ManyToManyField("Category")
    name = models.CharField(max_length=120)

    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)

    location = models.ForeignKey(Location, models.CASCADE)

    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    grassroot = models.ForeignKey(Grassroot, models.CASCADE)

    role = models.IntegerField(choices=(
        (1, 'founder'),
        (2, 'member'),
    ))


class LandingPage(TemplateMixin, MetaMixin):
    grassroot = models.OneToOneField(
        Grassroot, models.CASCADE, related_name="landing_page"
    )

    def __str__(self):
        return self.grassroot.name

    TEMPLATES = [
        Template(
            key="standard",
            title=_("standard"),
            template_name="pages/standard.html",
            regions=(
                Region(key="main", title=_("Main")),
            ),
        ),
        Template(
            key="with-sidebar",
            title=_("with sidebar"),
            template_name="pages/with-sidebar.html",
            regions=(
                Region(key="main", title=_("Main")),
                Region(key="sidebar", title=_("Sidebar"), inherited=True),
            ),
        ),
    ]


PagePlugin = create_plugin_base(LandingPage)


class RichText(plugins.richtext.RichText, PagePlugin):
    pass


class Image(plugins.image.Image, PagePlugin):
    pass
