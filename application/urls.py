from django.urls import path
from .views import ProposeProject, StudentProposalViewSet, DetailProposalViewSet, GetExcel, MentorProposalViewSet, GetAcceptedProposals, ProposalStatus, GetHODExcel, GetACExcel
#TODO: show only those proposals whose status is "not accepted"
mentor_proposal_list = MentorProposalViewSet.as_view({
    'get': 'list'
})

#show all the porposals submited by the student.
student_proposal_list = StudentProposalViewSet.as_view({
    'get': 'list'
})

proposal_detail = DetailProposalViewSet.as_view({
    'get': 'retrieve',
    'post': 'update'
})

accepted_proposal = GetAcceptedProposals.as_view({
    'get':'list'
})

urlpatterns = [
    path(r"propose/", ProposeProject.as_view(), name="propose-project"),
    path(r"proposal/mentor/<int:mentor__user_id>", mentor_proposal_list, name="mentor-proposal-list"),
    path(r"proposal/student/<int:id>", student_proposal_list, name="student-proposal-list"),
    path(r"proposal/detail/<str:pk>", proposal_detail, name="proposal-detail"),
    path(r"proposals/excel/accepted/<int:id>/status/<int:status>", GetExcel.as_view(), name="proposals-excel"),
    path(r"proposals/mentor/accepted/<int:mentor__user_id>",accepted_proposal,name="accepted-proposal"),
    path(r"proposal/mentor/<int:pk>/changestatus/<int:status>",ProposalStatus.as_view(),name="proposal_update"),
    path(r"proposal/excel/hod", GetHODExcel.as_view(), name="hod-excel"),
    path(r"proposal/excel/ac", GetACExcel.as_view(), name="ac-excel")
]