from django.shortcuts import render
from .forms import ProjectForm
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
import json


class ProposeProject(View):
    @csrf_exempt
    def post(self, request):
        form = ProjectForm(request.body)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'errors': ''}), status=200, content_type="application/json")
        else:
            return HttpResponse(json.dumps({'errors': form.errors}), status=400, content_type="application/json")
