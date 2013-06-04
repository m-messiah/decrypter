# ~*~ coding: utf-8 ~*~

# функция генерирующая 404 страницу
from django.http import Http404, HttpResponse

# функция отрисовки страницы, принимающая путь до шаблона
# и данные помещенные в шаблон
from django.shortcuts import render_to_response
from django.shortcuts import render

# наша модель
import cryptoanalyzis


def main_page(request):
    return render(request, 'index.html')


def decrypter(request):
    if 'encrypted' in request.POST:
        encrypted = request.POST['encrypted']
        decrypted = []
        for func in sorted(cryptoanalyzis.functions):
            try:
                decrypted.append(func(encrypted))
            except:
                continue
    else:
        return render(request, "input_form.html")

    return render_to_response('answer.html',
                              {"encrypted": request.POST['encrypted'],
                               "decrypted": dict(decrypted),
                               })
