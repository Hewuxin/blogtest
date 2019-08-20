from ..models import Post, Category
from django import template

register = template.Library()


@register.simple_tag
def get_recent_post(num=5):
    """
    最新文章模板标签
    :param num:
    :return:
    """
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    """
    归档模板标签
    :return:
    """
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """
    分类模板标签
    :return:
    """
    return Category.objects.all()

