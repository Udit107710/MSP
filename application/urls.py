from django.urls import path
from .views import ProposeProject, StudentProposalViewSet, DetailProposalViewSet, GetExcel, MentorProposalList

# mentor_proposal_list = MentorProposalViewSet.as_view({
#     'get': 'list'
# })

student_proposal_list = StudentProposalViewSet.as_view({
    'get': 'list'
})

proposal_detail = DetailProposalViewSet.as_view({
    'get': 'retrieve',
    'post': 'update'
})

urlpatterns = [
    path(r"propose/", ProposeProject.as_view(), name="propose-project"),
    path(r"proposal/mentor/<str:mentor__user__username>", MentorProposalList.as_view(), name="mentor-proposal-list"),
    path(r"proposal/student/<str:members>", student_proposal_list, name="student-proposal-list"),
    path(r"proposal/detail/<str:pk>", proposal_detail, name="proposal-detail"),
    path(r"proposals/excel/<str:username>", GetExcel.as_view, name="proposals-excel")
]