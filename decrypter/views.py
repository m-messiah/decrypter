from django.shortcuts import render_to_response
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.gzip import gzip_page
from glob import glob

try:
    from decrypter import cryptoanalyzis
except ImportError:
    import cryptoanalyzis

pictures = sorted([(f[f.rfind("/") + 1:f.rfind(".")], f)
                   for f in glob(settings.STATIC_ROOT + "abc/*")])

@gzip_page
def decrypter(request):
    if 'encrypted' in request.POST and request.POST['encrypted']:
        encrypted = request.POST['encrypted']
        print(("[INPUT]: %s" % encrypted).encode("utf8"))
        decrypted = []
        for func in cryptoanalyzis.functions:
            try:
                decrypted.append(func(encrypted))
            except Exception as e:
                decrypted.append((func.__name__, e))
        return render_to_response('answer.html',
                                  {"encrypted": request.POST['encrypted'],
                                   "decrypted": decrypted
                                   })

    return render(request, "input_form.html")

@gzip_page
def abc(request):
    return render(request, "abc.html", {"pictures": pictures})