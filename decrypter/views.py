# ~*~ coding: utf-8 ~*~

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.gzip import gzip_page

import cryptoanalyzis


@gzip_page
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
                                   "decrypted": decrypted
                                   })

    return render(request, "input_form.html")
