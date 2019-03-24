from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm
import markdown
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