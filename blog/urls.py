from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
	path(r'',views.IndexView.as_view(),name='index'),# 以空字符串开头且以空字符串结尾
	path(r'<int:pk>/detail/',views.PostDetailView.as_view(),name='detail'),
	path(r'archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archives'),
	path(r'category/<int:pk>/',views.CategoryView.as_view(),name='category'),
	path(r'tag/<int:pk>/',views.TagView.as_view(),name='tag'),
	path(r'MobileNetImage/',views.MobileNetImage),
	path(r'MobileNetWebcam/',views.MobileNetWebcam),
	path(r'TinyFaceDetectWebcam/',views.TinyFaceDetectWebcam),
	]