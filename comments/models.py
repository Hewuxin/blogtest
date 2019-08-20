from django.db import models
# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    # auto_now_add = True 自动把created_time的值指定为当前时间
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blogtest.Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]
