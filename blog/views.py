from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm
import markdown

from django.views.generic import ListView, DetailView
# Create your views here.
'''
需要 pip install markdown
	 pip install Pygments

'''

def index(request):
	post_list = Post.objects.all().order_by('-create_time')
	return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request,pk):
	post = get_object_or_404(Post,pk=pk)

	# 阅读量 +1
	post.increase_views()

	#markdown格式
	post.body = markdown.markdown(post.body,extensions=[
		'markdown.extensions.extra',
		'markdown.extensions.codehilite', #语法高亮拓展
		'markdown.extensions.toc', #自动生成目录
	])

	form = CommentForm()\
	#获取这篇Post下所有评论
	comment_list = post.comment_set.all()
	#模板变量
	context = {
		'post':post,
		'form':form,
		'comment_list':comment_list
	}

	return render(request, 'blog/detail.html',context={'post':post})

def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request,pk):
	cate = get_object_or_404(Category,pk=pk)
	post_list = Post.objects.filter(category=cate).order_by('-create_time')
	return render(request,'blog/index.html',context={'post_list':post_list})


class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	## 指定 paginate_by 开启分页功能
	paginate_by = 10

	def get_context_data(self,**kwargs):
		"""
		在视图函数中将模板变量通过render传递
		"""

		# 获得父类生成的传递给模板的字典
		context = super().get_context_data(**kwargs)

		# 父类已经有paginator_、age_obj、is_paginated三个模板变量，
		# paginator 是Paginator的一个实例
		# page_obj 是Page 的一个实例，
		# is-paginated 是一个bool变量，用于指示是否分页
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		# 调用自己写的pagination_data方法获得分页导航条需要的数据
		pagination_data = self.pagination_data(paginator,page,is_paginated)

		# 将分页导航页的模板变量更新到context中，注意pagination——data 方法返回的也是一个字典
		context.update(pagination_data)

		# 将更新后的context返回，以便ListView 使用这个变量
		# 注意此时context字典中已经有了显示分页导航条所需的数据
		return context

	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			# 如果没有分页就返回空
			return {}

		#  左边连续的页码号，初始值为空
		left = []

		# 右边连续的页码号，初始值为空
		right = []

		#标记第一页是否需要显示省略号
		left_has_more = False

		# 标识最后一页页码是否需要显示省略号
		right_has_more = False

		
		#第一个标签是否显示，初始为 False
		first = False

		#最后一个标签是否需要显示，初始为 False
		last = False

		# 获得用户当前请求的页码号
		page_number = page.number

		# 获得分页后的总数
		total_pages = paginator.num_pages

		# 获得整个分页页码列表
		page_range = paginator.page_range

		if page_number == 1:
			# 如果请求的是第一页的数据，那么left = []
			# 只需要右边的连续页码号
			right = page_range[page_number:page_number + 2]

			# 如果最右边的页码号比最后一页的页码号减去1还要小，
			# 说明最右边的页码号和最后一页的页码号之间还有其他页码
			if right[-1] < total_pages - 1:
				right_has_more = True

			# 判断是否需要显示最后一页的标签
			if right[-1] < total_pages:
				last = True
			
		elif page_number == total_pages:
			# 如果请求的是最后一页的数据，那么右边就不需要,right = []
			# 只要获取当其页码左边的页码号
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

			# 如果最左边的页码比第二页大
			# 说明 1~最左边页码之间需要省略号
			if left[0] > 2:
				left_has_more = True
			
			# 如果最左边的页码比第一页的大，说明需要显示第一页
			if left[0] > 1:
				first = True
			
		else:
			# 如果请求的既不是第一页也不是最后一页，获取左右两边连续页码
			# 获取当前页码左右两个连续页码
			left = page_range[(page_number - 3) if(page_number - 3)>0 else 0:page_number -1]
			right = page_range[page_number:page_number + 2] 

			# 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			# 是否需要显示第一页和第一页后的省略号
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
			
		data = {
			'left':left,
			'right':right,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more,
			'first':first,
			'last':last,
		}

		return data
			
class CategoryView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
		return super(CategoryView,self).get_queryset().filter(category=cate)


class ArchivesView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesView,self).get_queryset().filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
	

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	def get(self,request,*args,**kwargs):
		response = super(PostDetailView,self).get(request,*args,**kwargs)

		# 阅读量+1
		self.object.increase_views()
		return response

	def get_object(self,queryset=None):
		post = super(PostDetailView,self).get_object(queryset=None)
		post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])

		return post

	def get_context_data(self,**kwargs):
		context = super(PostDetailView,self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form':form,
			'comment_list':comment_list
		})
		return context

