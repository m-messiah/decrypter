# ~*~ coding: utf-8 ~*~

# функция генерирующая 404 страницу
from django.http import Http404, HttpResponse

# функция отрисовки страницы, принимающая путь до шаблона
# и данные помещенные в шаблон
from django.shortcuts import render_to_response
from django.shortcuts import render

import cryptoanalyzis
import coordinates


def about(request):
    return render(request, "about.html")


def decrypter(request):
    if 'encrypted' in request.POST and request.POST['encrypted']:
        encrypted = request.POST['encrypted']
        decrypted = []
        for func in sorted(cryptoanalyzis.functions):
            try:
                decrypted.append(func(encrypted))
            except:
                continue
        return render_to_response('answer.html',
                                  {"encrypted": request.POST['encrypted'],
                                   "decrypted": sorted(filter(lambda x:
                                                              len(x[0]) > 0,
                                                              decrypted))
                                   })
    elif 'coordinates' in request.POST and request.POST['coordinates']:
        coords = request.POST['coordinates']
        try:
            converted = coordinates.Coordinates(coords)
        except:
            pass
        else:
            return render_to_response('coords.html',
                                      {"coords": coords,
                                       "result":
                                       sorted(converted.allCoords.items())})

    return render(request, "input_form.html")
