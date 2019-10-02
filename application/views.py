from rest_framework import viewsets
from .forms import ProjectForm
from .models import Project
from .serializers import ProjectProposalSerializer, ProjectDetailProposalSerializer
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
import csv
import json


class ProposeProject(View):
    @csrf_exempt
    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'errors': ''}), status=200, content_type="application/json")
        else:
            return HttpResponse(json.dumps({'errors': form.errors}), status=400, content_type="application/json")


class MentorProposalViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectProposalSerializer
    lookup_field = 'mentor__username'


class StudentProposalViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectProposalSerializer
    lookup_field = 'members'


class DetailProposalViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailProposalSerializer
    lookup_field = 'pk'


class GetExcel(APIView):
    def get(self, request, username):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sheet.csv"'
        writer = csv.writer(response)
        projects = list(Project.objects.filter(mentor__username=username).defer('mentor'))
        fields = ['project_type', 'title', 'abstract', 'proposal', 'associated_files', 'status', 'members']
        writer.writerow(fields)

        for project in projects:
            writer.writerow(project)

        return response