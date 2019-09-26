from django.urls import path
from .views import ProposeProject, MentorProposalViewSet, StudentProposalViewSet

mentor_proposal_list = MentorProposalViewSet.as_view({
    'get': 'list'
})

student_proposal_list = StudentProposalViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    path(r"propose/", ProposeProject.as_view(), name="propose-project"),
    path(r"proposal/mentor/<str:mentor>", mentor_proposal_list, name="mentor-proposal-list"),
    path(r"proposal/student/<str:members", student_proposal_list, name="student-proposal-list"),
]