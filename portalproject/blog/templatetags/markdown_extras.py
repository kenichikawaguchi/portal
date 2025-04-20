# myapp/templatetags/markdown_extras.py
from django import template
from markdownx.utils import markdownify

register = template.Library()

@register.filter(is_safe=True)
def md_preview_first_line(value):
    """
    改行で分割して最初の行だけ markdownify する
    """
    text = value or ""
    first_line = text.splitlines()[0] if text else ""
    return markdownify(first_line)

