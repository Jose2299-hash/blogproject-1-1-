from django.urls import path, include
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView
from  . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'blogapp'


urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('registro/', views.registro, name="registro"),
    path('login/', views.inicio_sesion, name='login'),
    path('logout/', views.Cerrar_sesion, name='logout'),
    path('ckeditor/', include('ckeditor_uploader.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)