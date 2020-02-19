
from django import template
from django.urls import translate_url as django_translate_url
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    path = context.get('request').get_full_path()
    return django_translate_url(path, lang_code)


@register.filter()
def format_text(text, arg):
    return mark_safe(text.format(arg))
