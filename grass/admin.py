from django.contrib import admin

from content_editor.admin import ContentEditor
from feincms3 import plugins

from grass import models

# Register your models here.


@admin.register(models.LandingPage)
class LandingPageAdmin(ContentEditor):

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
    ]
