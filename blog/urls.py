from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('emoji/upload/', views.emoji_upload, name='emoji_upload'),
    path('emoji/<int:pk>/delete/', views.emoji_delete, name='emoji_delete'),
    path('sticker/upload/', views.sticker_upload, name='sticker_upload'),
    path('sticker/<int:pk>/delete/', views.sticker_delete, name='sticker_delete'),
    path('font/upload/', views.font_upload, name='font_upload'),
    path('font/<int:pk>/delete/', views.font_delete, name='font_delete'),
    path('export/media/json/', views.export_media_json, name='export_media_json'),
    path('dynamic_fonts_css/', views.dynamic_fonts_css, name='dynamic_fonts_css'),
    path('dynamic_fonts_list/', views.dynamic_fonts_list, name='dynamic_fonts_list'),
    path('api/media/', views.get_media_json, name='get_media_json'), # New API endpoint
]
