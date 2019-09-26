from django.urls import path
from .views import ProposeProject, ProposalViewSet

proposal_list = ProposalViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    path(r"propose/", ProposeProject.as_view(), name="propose-project"),
    path(r"proposal/<str:mentor>", proposal_list, name="proposal-list"),
]