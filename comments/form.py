from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment   # 表明这个表对应的数据库类型是Comment类
        fields = ['name', 'email', 'url', 'text']  # 指定表单需要显示的字段
