from django.shortcuts import render_to_response
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.gzip import gzip_page
from os import walk

try:
    from decrypter import cryptoanalyzis
except ImportError:
    import cryptoanalyzis


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

@gzip_page
def abc(request):
    pictures = []
    for (_, _, filenames) in walk(settings.STATIC_ROOT + "abc/"):
        for filename in filenames:
            pictures.append((filename[:filename.rfind(".")], "/static/abc/{0}".format(filename)))
    return render(request, "abc.html")