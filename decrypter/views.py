# ~*~ coding: utf-8 ~*~

from django.shortcuts import render_to_response
from django.shortcuts import render

import cryptoanalyzis
import coordinates


def decrypter(request):
    if 'encrypted' in request.POST and request.POST['encrypted']:
        encrypted = request.POST['encrypted']
        try:
            print "[INPUT]: {}".format(encrypted)
        except UnicodeEncodeError:
            print "[INPUT]: {}".format(" ".join(map(str, map(ord, encrypted))))
        decrypted = []
        for func in cryptoanalyzis.functions:
            try:
                decrypted.append(func(encrypted))
            except:
                continue
        return render_to_response('answer.html',
                                  {"encrypted": request.POST['encrypted'],
                                   "decrypted": filter(lambda x:
                                                       len(x[0]) > 0,
                                                       decrypted)
                                   })
    elif (('coordinates1' in request.POST and request.POST['coordinates1'])
          and ('coordinates2' in request.POST and request.POST['coordinates2'])
          ):
        coords = request.POST['coordinates1'], request.POST['coordinates2']
        try:
            print "[INPUT]: {}".format(coords)
        except UnicodeEncodeError:
            print "[INPUT]: {}".format(" ".join(map(str, map(ord, coords))))
        try:
            converted = coordinates.Coordinates(coords)
        except:
            pass
        else:
            return render_to_response('coords.html',
                                      {"coords": coords,
                                       "result":
                                       sorted(converted.all_coords.items())})

    return render(request, "input_form.html")
