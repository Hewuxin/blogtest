from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
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
