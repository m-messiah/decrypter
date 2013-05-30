# ~*~ coding: utf-8 ~*~

# функция генерирующая 404 страницу
from django.http import Http404, HttpResponse

# функция отрисовки страницы, принимающая путь до шаблона
# и данные помещенные в шаблон
from django.shortcuts import render_to_response
from django.shortcuts import render

# наша модель
from models import Crypto
import cryptoanalyzis


def main_page(request):
    return HttpResponse('''<!DOCTYPE html>
        <html>
            <head><title>Messiah's home</title></head>
            <body><h1>Nothing interesting here</h1></body>
        </html>''')


def decrypter(request):
    return render(request, 'input_form.html')


def generate(request):
    if 'encrypted' in request.POST:
        encrypted = request.POST['encrypted']
        decrypted = []
        for func in cryptoanalyzis.functions:
            try:
                decrypted.append(func(encrypted))
            except:
                continue
    else:
        decrypted = {"Bad request": 'You submitted an empty form.'}

    return render_to_response('answer.html',
                              {"encrypted": request.POST['encrypted'],
                               "decrypted": dict(decrypted),
                               })


def get_post(request, post_id):
    try:
        # выбираем конкретный пост, pk - primary key
        post = Crypto.objects.get(pk=post_id)
    except Crypto.DoesNotExist:
        # если такого поста нет, то генерируем 404
        raise Http404

    # отрисовываем
    return render_to_response('single.html',
                              {"title": post.title, "text": post.text})
