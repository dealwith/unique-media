import json
import six
from cloudinary import api
from cloudinary.forms import cl_init_js_callbacks
from django.http import HttpResponse
from django.shortcuts import render
from .forms import PhotoForm, PhotoDirectForm, PhotoUnsignedDirectForm
from .models import Photo


def filter_nones(d):
    return dict((k, v) for k, v in six.iteritems(d) if v is not None)


def list(request):
    defaults = dict(format="jpg", height=150, width=150)
    defaults["class"] = "thumbnail inline"
    
    samples = [
        dict(crop="fill", radius=10),
        dict(crop="scale"),
        dict(crop="fit", format="png"),
        dict(crop="thumb", gravity="face"),
        dict(format="png", angle=20, height=None, width=None, transformation=[
            dict(crop="fill", gravity="north", width=150, height=150, effect="sepia"),
        ]),
    ]
    samples = [filter_nones(dict(defaults, **sample)) for sample in samples]
    return render(request, 'list.html', dict(photos=Photo.objects.all(), samples=samples))


def upload(request):
    unsigned = request.GET.get("unsigned") == "true"

    if (unsigned):
        try:
            api.upload_preset(PhotoUnsignedDirectForm.upload_preset_name)
        except api.Notfound:
            api.create_upload_preset(name=PhotoUnsignedDirectForm.upload_preset_name, unsigned=True,
                                     folder="preset_folder")

    direct_form = PhotoUnsignedDirectForm() if unsigned else PhotoDirectForm()
    context = dict(
        backend_form=PhotoForm(),
        direct_form=direct_form,
        unsigned=unsigned,
    )

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            form.save()
    return render(request, 'upload.html', context)


def direct_upload_complete(request):
    form = PhotoDirectForm(request.POST)
    if form.is_valid():
        form.save()
        ret = dict(photo_id=form.instance.id)
    else:
        ret = dict(erroes=form.errors)
    return HttpResponse(json.dumps(ret), content_type='application/json')