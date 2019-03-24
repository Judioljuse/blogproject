from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

# Create your models here.
class Category(models.Model):
	'''
	CharField 指定了分类名 name 的数据类型，CharField 是字符
	max_length =100规定长度
	'''
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name


class Tag(models.Model):
	'''
	标签类
	'''
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Post(models.Model):
	'''
	文章数据库
	'''
	#文章标题
	title = models.CharField(max_length=70)

	#文章正文
	body = models.TextField()

	#创建时间 和 最后一次修改时间
	create_time = models.DateTimeField()
	modified_time = models.DateTimeField()


	#文章摘要，balnk允许空值
	excerpt = models.CharField(max_length=200,blank=True)

	## 分类数据库 和 标签数据库的 关联
	#ForeignKey一对多的关系
	#ManyToManyField 多对多的关系
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag,blank=True)


	#文章作者
	author = models.ForeignKey(User,on_delete=models.CASCADE)

	#阅读量
	views = models.PositiveIntegerField(default = 0) # 初始值为0

	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blog:detail", kwargs={"pk": self.pk})

	class Meta:
		ordering = ['create_time']
	