from django import template

register = template.Library()

@register.filter
def make_range(value):
    """
    创建一个从1到value的范围，用于生成数量选择选项
    """
    return range(1, value + 1)