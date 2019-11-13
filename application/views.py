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
from accounts.models import Teacher


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
                return HttpResponse(json.dumps({'errors': "member does not exits or is locked "+str(sap_2)+" "+str(sap_3)+" "+str(sap_4)}), status=400, content_type="application/json")
            proposal.save()
            return HttpResponse(json.dumps({'errors': ''}), status=200, content_type="application/json")
        else:
            return HttpResponse(json.dumps({'errors': form.errors}), status=400, content_type="application/json")


class MentorProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectProposalSerializer

    def get_queryset(self):
        queryset = Project.objects.order_by('updated_at').filter(mentor__user_id=self.kwargs['mentor__user_id']).filter(status=0)
        result = []
        for item in queryset:
            flag = True
            for member in item.members:
                if member.lock == 1:
                    flag = False
                    break
            if flag:
                result.append(item)
        return result


class StudentProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectProposalSerializer

    def get_queryset(self):
        qset1 = Project.objects.filter(member1_id=self.kwargs['id'])
        qset2 = Project.objects.filter(member2_id=self.kwargs['id'])
        qset3 = Project.objects.filter(member3_id=self.kwargs['id'])
        qset4 = Project.objects.filter(member4_id=self.kwargs['id'])
        qset = (qset1 | qset2 | qset3 | qset4).order_by('updated_at').reverse()
        return qset
        

class DetailProposalViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailProposalSerializer
    lookup_field = 'pk'


class GetExcel(APIView):
    def get(self, request, id, status):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sheet.csv"'
        writer = csv.writer(response)
        #projects = list(Project.objects.filter(mentor__user__username=username).defer('mentor'))
        # projects = list(Project.objects.all().defer('mentor'))
        projects = list(Project.objects.order_by('created_at').filter(mentor_id=id).filter(status=status).reverse())
        fields = ['Project Type', 'Title', 'Description', 'proposal', 'associated_files', 'Status', 'member1','member2','Mentor']
        writer.writerow(fields)

        for project in projects:
            row=[project.project_type, project.title, project.abstract, project.proposal, project.associated_files, project.status, project.member1.user.first_name, project.member2.user.first_name, project.mentor.user.first_name+" "+project.mentor.user.last_name]
            writer.writerow(row)
        return response


class GetAcceptedProposals(viewsets.ModelViewSet):
    serializer_class = ProjectProposalSerializer

    def get_queryset(self):
        return Project.objects.order_by('updated_at').filter(mentor__user_id=self.kwargs['mentor__user_id']).filter(status=1).reverse()


class ProposalStatus(APIView):
    serializer_class = ProjectProposalSerializer

    def put(self,request,status, pk):
        try:
            proposal = Project.objects.get(pk=pk)
            if status == 0:
                proposal.status = 0
            elif status == 1:
                proposal.status = 1
            elif status == 2:
                for member in proposal.members:
                    if member.lock == 1:
                        return HttpResponse(json.dumps({'errors': { 'Member Locked' : member.sap_id}}),status=400, content_type="application/json")
                proposal.status = 2
                for member in proposal.members:
                    member.lock = 1
            else:
                return HttpResponse(json.dumps({'errors':'Invalid status sent'}),status=400,content_type="application/json")
            mentor = Teacher.objects.get(pk=proposal.mentor_id)
            if(mentor.slots_occupied==5):
                return HttpResponse(json.dumps({'errors':'Mentor slots_occupied are full'}),status=400,content_type="application/json")
            mentor.slots_occupied = mentor.slots_occupied+1
            mentor.save()
            proposal.save()
            #lock the student if proposal is accepted
            if proposal.status == 1:
                memberlist = []
                if proposal.member1!=None:
                    memberlist.append(proposal.member1)
                if proposal.member2!=None:
                    memberlist.append(proposal.member2)
                if proposal.member3!=None:
                    memberlist.append(proposal.member3)
                if proposal.member4!=None:
                    memberlist.append(proposal.member4)
                
                for member in memberlist:
                    member_obj = Student.objects.get(pk=member.user_id)
                    member_obj.lock=1
                    member_obj.save()

            return HttpResponse(json.dumps({'errors': ''}), status=200, content_type="application/json")
        except Project.DoesNotExist:
            return HttpResponse(json.dumps({'errors': 'Object does not exist'}), status=404, content_type="application/json")


class GetHODExcel(APIView):
    def get(self, request):
        user = request.user
        hod = Teacher.objects.get(user__username=user.username)
        department = hod.department
        data = Project.objects.filter(mentor__department=department)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sheet.csv"'
        writer = csv.writer(response)
        fields = ["Project ID", "Faculty Name", "No of projects per faculty", "Title", "Student 1", "Student 2", "Student 3", "Student 4"]
        writer.writerow(fields)

        # for project in projects:
        #     row=[project.project_type, project.title, project.abstract, project.proposal, project.associated_files, project.status, project.member1.user.first_name, project.member2.user.first_name, project.mentor.user.first_name+" "+project.mentor.user.last_name]
        #     writer.writerow(row)
        for info in data:
            if info.member4:
                row = [info.id, info.mentor.user.username, info.mentor.slots_occupied, info.title,
                       [info.member1.user.first_name, info.member1.program, info.member1.sap_id],
                       [info.member2.user.first_name, info.member2.program, info.member2.sap_id],
                       [info.member3.user.first_name, info.member3.program, info.member3.sap_id],
                       [info.member4.user.first_name, info.member4.program, info.member4.sap_id]]
            else:
                row = [info.id, info.mentor.user.username, info.mentor.slots_occupied, info.title,
                       [info.member1.user.first_name, info.member1.program, info.member1.sap_id],
                       [info.member2.user.first_name, info.member2.program, info.member2.sap_id],
                       [info.member3.user.first_name, info.member3.program, info.member3.sap_id],]
            writer.writerow(row)
        return response