import urllib.parse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages


BLOG_TOPIC = [
    'Искусственные нейронные сети',
    'Тестирование информационных систем',
    'Стандартизация',
    'Разработки Web-приложений на Python'
]

BLOG_POSTS = [
    {
        'title': 'Как создать REST API на FastAPI за 15 минут',
        'content': 'Пошаговое руководство по созданию быстрого и эффективного API с использованием современного фреймворка FastAPI.',
        'category': 'Разработки Web-приложений на Python',
        'date': '26.09.2025'
    },
    {
        'title': 'Введение в нейросети: с нуля до первого проекта',
        'content': 'Разбираемся, как работают нейросети, и создаём простую модель на TensorFlow.',
        'category': 'Искусственные нейронные сети',
        'date': '25.09.2025'
    },
    {
        'title': 'Основы кибергигиены: 5 правил для каждого пользователя',
        'content': 'Простые, но эффективные меры защиты ваших данных в интернете.',
        'category': 'Тестирование информационных систем',
        'date': '24.09.2025'
    },
    {
        'title': 'Как создать техническое задание за 15 минут с помощью ChatGPT',
        'content': 'Для этого вам нужно всего лишь...',
        'category': 'Стандартизация',
        'date': '23.09.2025'
    }
]


def index(request):
    encoded_categories = request.COOKIES.get('categories', '')

    if encoded_categories:
        categories_str = urllib.parse.unquote(encoded_categories)
        selected_list = categories_str.split(',')
    else:
        selected_list = []

    filtered_posts = [
        posts for posts in BLOG_POSTS
        if not selected_list or posts['category'] in selected_list
    ]

    context = {
        'categories': BLOG_TOPIC,
        'posts_list': filtered_posts,
        'selected_categories': selected_list
    }

    response = render(request, 'blog_index.html', context)

    return response


def save_preferences(request):
    if request.method == 'POST':
        categories = request.POST.getlist('categories')
        language = request.POST.get('language', 'ru')

        categories_str = ','.join(categories)
        encoded_categories = urllib.parse.quote(categories_str, safe='')

        response = redirect('blog:home')

        response.set_cookie('categories', encoded_categories, max_age=365*24*60*60)

        messages.success(request, 'cookies success')

        return response

    return redirect('blog:home')