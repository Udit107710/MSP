from rest_framework import serializers
from .models import Project, Team
from accounts.serializers import UserSerializer


class ProjectProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('associated_files', 'status')


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(many=True, slug_field='username')
    project = serializers.SlugRelatedField(slug_field='title')

    class Meta:
        model = Team
        fields = '__all__'