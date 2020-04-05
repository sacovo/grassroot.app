from django.utils.html import format_html, mark_safe

from feincms3.renderer import TemplatePluginRenderer

from .models import LandingPage, RichText, Image


renderer = TemplatePluginRenderer()

renderer.register_string_renderer(
    RichText,
    lambda plugin: mark_safe(plugin.text),
)

renderer.register_template_renderer(
    Image,
    'plugins/image.html',
)
