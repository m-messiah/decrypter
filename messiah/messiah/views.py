# ~*~ coding: utf-8 ~*~

# функция генерирующая 404 страницу
from django.http import Http404

# функция отрисовки страницы, принимающая путь до шаблона и данные помещенные в шаблон
from django.shortcuts import render_to_response

# наша модель
from messiah.models import Post

def main_page (request):
    # Получаем список постов
    posts = Post.objects.all()
    # отрисовываем
    return render_to_response('list.html', {"posts":  posts})

def get_post (request, post_id):
    try:
        # выбираем конкретный пост, pk - primary key
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        # если такого поста нет, то генерируем 404
        raise Http404

    # отрисовываем
    return render_to_response('single.html', {"title":  post.title, "text": post.text})
