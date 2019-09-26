from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Project
from accounts.serializers import UserSerializer


class ProjectProposalSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    mentor = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Project
        exclude = ('associated_files', 'proposal')