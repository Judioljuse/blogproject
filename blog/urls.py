from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
	path(r'',views.index,name='index'),# 以空字符串开头且以空字符串结尾
	path(r'<int:pk>/detail/',views.detail,name='detail'),
	path(r'archives/<int:year>/<int:month>/', views.archives, name='archives'),
	path(r'category/<int:pk>/',views.category,name='category'),
	]