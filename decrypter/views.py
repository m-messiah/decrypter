from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.gzip import gzip_page

from decrypter import cryptoanalyzis


@gzip_page
def decrypter(request):
    if 'encrypted' in request.POST and request.POST['encrypted']:
        encrypted = request.POST['encrypted']
        print("[INPUT]: {}".format(encrypted).encode("utf8"))
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
