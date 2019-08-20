from django.shortcuts import render, get_object_or_404
from .models import Post, Category
import markdown
from comments.form import CommentForm

# Create your views here.


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blogtest/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',   # 本身包含很多拓展
                                      'markdown.extensions.codehilite',  # 语法高亮，为实现代码高亮功能提供基础
                                      'markdown.extensions.toc',   # 自动生成目录
                                  ])
    form = CommentForm()
    # 获取这篇post下的全部评论
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list}
    return render(request, 'blogtest/detail.html', context=context)


def archives(request, year, month):
    """
    由于这里作为函数的参数列表，所以把点换成两个下划线，即created_time__year
    :param request:
    :param year:
    :param month:
    :return:
    """
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blogtest/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blogtest/index.html', context={'post_list': post_list})
