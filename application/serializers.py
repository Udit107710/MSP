from rest_framework import serializers
from .models import Project
from accounts.serializers import UserSerializer


class ProjectProposalSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(slug_field='user__username', many=True, read_only=True)
    mentor = serializers.SlugRelatedField(slug_field='user__username', many=False, read_only=True)

    class Meta:
        model = Project
        exclude = ('associated_files', 'proposal')