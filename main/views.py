from django.http import HttpResponse
import openai
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.translation import activate
from .models import Article
from django.utils import timezone
from django.urls import translate_url
from django.utils.translation import activate, get_language
from django.shortcuts import redirect
from .models import Article, Category

def index(request):
    articles = Article.objects.all()
    query = request.GET.get('q')
    results = []
    if query:
        results = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    response = None
    if request.method == 'POST':
        user_message = request.POST.get('message')
        openai.api_key = settings.OPENAI_API_KEY
        try:
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Utilisez "gpt-4" ou tout autre modèle que vous préférez
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ]
            )
            response = completion.choices[0].message.content
        except openai.OpenAIError as e:
            response = f"Error: {e}"

    return render(request, 'main/index.html', {
        'articles': articles,
        'query': query,
        'chat_response': response
    })

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'main/article_detail.html', {'article': article})

def change_language(request, language):
    activate(language)
    response = redirect(request.META.get('HTTP_REFERER', 'index'))
    response.set_cookie('django_language', language)
    return response


def article_create(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_id)
        Article.objects.create(title=title, content=content, author=author, category=category)
        return redirect('list_articles')
    return render(request, 'main/create_article.html', {'categories':categories})

def list_articles(request):
    articles = Article.objects.all()
    return render(request, 'main/list_articles.html', {'articles': articles})

def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    categories = Category.objects.all()
    if request.method == "POST":
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.author = request.POST.get('author')
        category_id = request.POST.get('category')
        article.category = get_object_or_404(Category, pk=category_id)
        article.save()
        return redirect('article_detail', article_id=article.id)
    return render(request, 'articles/create_article.html', {'article': article, 'categories': categories})

def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        article.delete()
        return redirect('list_articles')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})

def search(request):
    # Your search logic
    return render(request, 'search_results.html', {'results': 'results'})
def chatbot(request):
    response = None
    if request.method == 'POST':
        user_message = request.POST.get('message')
        openai.api_key = settings.OPENAI_API_KEY
        try:
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Utilisez "gpt-4" ou tout autre modèle que vous préférez
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ]
            )
            response = completion.choices[0].message.content
        except openai.OpenAIError as e:
            response = f"Error: {e}"

    return HttpResponse(response)