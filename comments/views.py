from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request,post_pk):
    post = get_object_or_404(Post,pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid(): #检查表单是否符合格式要求
            comment = form.save(commit=False)

            #将评论和文章关联
            comment.post = post
            #将评论数据保存进数据库
            comment.save()

            #重定向回到post详情页
            return redirect(post)

        else:
            comment_list = post.comment_set.all()
            context = {'post':post,
                        'form':form,
                        'comment_list':comment_list}

            return render(request,'blog/detail.html',context=context)

    return redirect(post)        

        