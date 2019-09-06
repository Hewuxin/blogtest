from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count


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
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts_gt=0)


@register.simple_tag
def get_categories():
    # 在顶部引入Count函数
    # count计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    """
    获取标签云
    :return:
    """
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
