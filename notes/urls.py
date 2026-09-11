from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/delete',views.delete, name='delete'),
    path('<int:id>/update', views.update, name='update'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:id>/', views.tag_detail, name='tag_detail'),
]