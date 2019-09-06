from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown
from comments.form import CommentForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
# Create your views here.


class IndexView(ListView):
    """
    从数据库中获取文章(Post)列表，
    ListView就是从数据库中获取某个模型列表数据的
    """
    model = Post
    template_name = 'blogtest/index.html'
    context_object_name = 'post_list'
    # 指定paginate_by属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 1

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给render函数的context参数传递一个字典实现的，
        在类视图中，这个需要传递的模板变量字典是通过get_context_data获得的
        覆写该方法，以便能够自己插入一些自定义的模板变量进去。
        :param kwargs:
        :return:
        """
        # 首先获取父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中，已有paginator、page_obj、is_paginated这三个吗模板变量
        # paginator是Paginator的一个实例
        # page_obj 是Page的一个实例
        # is_paginated 是一个布尔变量，用于指示是否分页
        # 由于context是一个字典，所以调用get方法从中抽取某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的pagination_data 方法获取显示分页导航条需要的数据。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到context中，注意pagination_data返回返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的context 返回，以便ListView使用这个字典中的模板变量去渲染模板。
        # 注意此时context字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航，不用任何分页导航条的数据，因此返回一个空的字典
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []
        # 当前页右边连续的页码号，初始值为空
        right = []
        # 表示第 1 页 页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第1 页的页码号
        # 因为如果当前页左边的连续页码号中已经含有第1 页的页码号，此时就无需再显示第一页的页码号，
        # 其他情况下第一页的页码是始终需要显示的
        # 初始值为False
        first = False

        #  标示是否需要显示最后一页的页码号
        # 需要此指示变量的理由和上面相同
        last = False

        # 获取用户当前请求的页码号
        page_number = page.number

        # 获取分页总数
        total_pages = paginator.num_pages

        # 获取整个分页页码列表，比如分了四页 就是[1,2,3,4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此left = [](已默认为空)
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是[1, 2, 3, 4], 那么获取的就是 right = 【2，3】
            # 注意这里只获取了当前页后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去1还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其他页码，因此需要显示省略号，通过right_has_more来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过last来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right = [] (以默认为空)
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是[1,2,3,4]，那么获取的就是left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]

            # 如果最左边的页码号比第2页页码还大，
            # 说明最左边的页码号和第1页的页码号之间还有其他页码，因此需要显示省略号，通过left_has_more来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第1 页的页码还大，说明当前页左边的连续页码号中不包含第一页的页码。
            # 所以需要显示第一页的页码号，通过first来指示。
            if left[0] > 1:
                first = True

        else:
            # 用户请求的既不是最后一页，也不是第 1页， 则需要获取当前页左右两边的连续页码号
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number: page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页 和第一页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogtest/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        """
        覆写get方法的目的是因为每当文章被访问一次，就得将文章阅读量+1
        get方法返回的是一个HttpResponse实例
        之所以需要先调用父类的get方法，是因为只有当get方法被调用后，才有
        self.object 属性，其值为Post模型实例，即被访问的文章post
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量+1
        # 注意 self.object 的值就是被访问的文章post
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对post的body值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          TocExtension(slugify=slugify),
                                      ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        """
        目的是因为除了将post传递给模板外(DetailView 已经帮我们完成),
        还要把评论表单、post下的评论列表传递给模板。
        :param kwargs:
        :return:
        """
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


# def archives(request, year, month):
#     """
#     由于这里作为函数的参数列表，所以把点换成两个下划线，即created_time__year
#     :param request:
#     :param year:
#     :param month:
#     :return:
#     """
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     return render(request, 'blogtest/indexes.html', context={'post_list': post_list})


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        """
        该方法默认获取指定模型的全部列表数据
        在类视图中，从URL捕获的命名组参数值保存在实例的kwrags属性里
        非命名组参数值保存在实例的args属性
       :return:
        """
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    model = Post
    template_name = 'blogtest/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blogtest/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blogtest/index.html', {'error_msg': error_msg,
                                                   'post_list': post_list})

