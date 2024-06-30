
from django.urls import path
from .views import list_articles, article_detail, article_create, article_update, change_language, article_delete, index, search, chatbot

urlpatterns = [
    path('', index, name='index'),
    path('articles/', list_articles, name='list_articles'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('article/create/', article_create, name='article_create'),
    path('article/<int:article_id>/update/', article_update, name='article_update'),
    ###path('article/<int:article_id>/delete/', article_delete, name='article_delete'),
    path('change_language/<str:language>/', change_language, name='change_language'),
    path('article/<int:article_id>/delete/', article_delete, name='article_delete'),
    path('search/', search, name='search'),
    path('chatbot/', chatbot, name='chatbot'),
]