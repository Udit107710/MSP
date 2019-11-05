from rest_framework import viewsets
from .forms import ProjectForm
from .models import Project
from .serializers import ProjectProposalSerializer, ProjectDetailProposalSerializer
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
import csv
import json
from itertools import chain
from accounts.models import Student



class ProposeProject(View):
    @csrf_exempt
    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        
        if form.is_valid():
            proposal = form.save(commit=False)
            sap_2 = request.POST.get('member2_sapid',-1)
            sap_3 = request.POST.get('member3_sapid',-1)
            sap_4 = request.POST.get('member4_sapid',-1)
            
            try:
                if sap_2!=-1:
                    proposal.member2 = Student.objects.filter(lock=0).get(sap_id=sap_2)
                if sap_3!=-1:
                    proposal.member3 = Student.objects.filter(lock=0).get(sap_id=sap_3)
                if sap_4!=-1:
                    proposal.member4 = Student.objects.filter(lock=0).get(sap_id=sap_4)
            except Student.DoesNotExist:
                return HttpResponse(json.dumps({'errors': "member does not exits or is locked"+sap_2+":"+sap_3}), status=400, content_type="application/json")
            proposal.save()
            return HttpResponse(json.dumps({'errors': ''}), status=200, content_type="application/json")
        else:
            return HttpResponse(json.dumps({'errors': form.errors}), status=400, content_type="application/json")


class MentorProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectProposalSerializer
    def get_queryset(self):
        queryset = Project.objects.order_by('updated_at').filter(mentor__user_id=self.kwargs['mentor__user_id']).filter(status=0)
        return queryset

# class MentorProposalList(View):
#     @csrf_exempt
#     def get(self, request, mentor__user__username):
#         proposals = list(Project.objects.all().select_related('mentor__user').filter(mentor__user__username=mentor__user__username).defer('associated_files', 'proposal'))
#         print(proposals)
#         serializer = ProjectProposalSerializer(data=proposals, many=True)
#         if serializer.is_valid():
#             return HttpResponse(serializer, status=200, content_type="application/json")
#         else:
#             print(serializer.errors)
#             return HttpResponse("errors", status=200, content_type="application/json")


class StudentProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectProposalSerializer

    def get_queryset(self):
        qset1 = Project.objects.order_by('updated_at').filter(member1_id=self.kwargs['id'])
        qset2 = Project.objects.order_by('updated_at').filter(member2_id=self.kwargs['id'])
        qset3 = Project.objects.order_by('updated_at').filter(member3_id=self.kwargs['id'])
        qset4 = Project.objects.order_by('updated_at').filter(member4_id=self.kwargs['id'])
        qset = list(chain(qset1,qset2,qset3,qset4))
        return qset
        


class DetailProposalViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailProposalSerializer
    lookup_field = 'pk'


class GetExcel(APIView):
    def get(self, request,id,status):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sheet.csv"'
        writer = csv.writer(response)
        #projects = list(Project.objects.filter(mentor__user__username=username).defer('mentor'))
        # projects = list(Project.objects.all().defer('mentor'))
        projects = list(Project.objects.order_by('created_at').filter(mentor_id=id).filter(status=status))
        fields = ['Project Type', 'Title', 'Description', 'proposal', 'associated_files', 'Status', 'members','Mentor']
        writer.writerow(fields)

        for project in projects:
            row=[project.project_type,project.title,project.abstract,project.proposal,
            project.associated_files,project.status,project.members,project.mentor.user.first_name+" "+project.mentor.user.last_name]
            writer.writerow(row)
        return response

class GetAcceptedProposals(viewsets.ModelViewSet):
    serializer_class = ProjectProposalSerializer
    def get_queryset(self):
        return Project.objects.order_by('updated_at').filter(mentor__user_id=self.kwargs['mentor__user_id']).filter(status=1)

class ProposalStatus(APIView):
    serializer_class = ProjectProposalSerializer
    def put(self,request,*args,**kwargs):
        try:
            proposal = Project.objects.get(pk=kwargs['id'])
            if kwargs['status']==0:
                proposal.status=0
            elif kwargs['status']==1:
                proposal.status=1
            elif kwargs['status']==2:
                proposal.status=2
            else:
                return HttpResponse(json.dumps({'errors':'Invalid status sent'}),status=400,content_type="application/json")
            proposal.save()
            return HttpResponse(json.dumps({'errors': ''}), status=200, content_type="application/json")
        except Project.DoesNotExist:
            return HttpResponse(json.dumps({'errors': 'Object does not exist'}), status=400, content_type="application/json")


        