from django.shortcuts import render, get_object_or_404, redirect
from blogtest.models import Post

from .models import Comment
from .form import CommentForm


# Create your views here.


def post_comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        # 调用form.is_valid()方法，django自动检查表单的数据是否符合格式要求
        if form.is_valid():
            # 检查到数据是合法的，调用表单的save方法保存到数据库
            # commit = False 的作用是仅仅利用表单的数据生成Comment模型类的实例，但还不保存评论数据到数据库
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来
            comment.post = post

            # 最终将评论数据保存进数据库，调用模型实例的save方法
            comment.save()

            # 重定向到post的详情页，实际上当redirect函数接收一个模型的实例时，它会调用这个模型实例的get_absolute_url方法，
            # 然后重定向到get_absolute_url方法返回URL
            return redirect(post)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            comment_list = post.comment_set.all()   # 等价于 Comment.objects.filter(post=post)
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list}
            return render(request, 'blogtest/detail.html', context=context)
    # 不是post请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)
