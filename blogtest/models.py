from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签Tag
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章的数据库表
    """
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()  # 创建时间
    modified_time = models.DateTimeField()  # 最后一次修改时间
    excerpt = models.CharField(max_length=200, blank=True)  # 文章摘要 blank=True允许空值

    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 一对多
    tags = models.ManyToManyField(Tag, blank=True)  # 多对多

    # 文章作者 User从django.contrib.models导入
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)   # 值只允许为正整数或0

    def __str__(self):
        return self.title

    # 自定义get_absolute_url方法
    def get_absolute_url(self):
        return reverse('blogtest:detail', kwargs={'pk': self.pk})

    class Meta:
        """
        指定排序属性,负号表示逆序排列
        """
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        """
        通过复写模型的save方法，载数据被保存到数据库前，先从body字段
        摘取N个字符保存到excerpt字段中，从而实现自动摘要。
        :param args:
        :param kwargs:
        :return:
        """
        if not self.excerpt:
            # 首先实例化一个Markdown类，用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将Markdown文本渲染成HTML文本
            # strip_tags 去掉HTML 文本的全部HTML标签
            # 从文本摘取前54个字符赋给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

