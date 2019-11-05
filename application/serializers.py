from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Project
from accounts.serializers import UserSerializer
from accounts.serializers import StudentSerializer
from accounts.serializers import TeacherSerializer


class ProjectProposalSerializer(serializers.ModelSerializer):
    member1 = StudentSerializer(many=False,read_only=True)
    member2 = StudentSerializer(many=False,read_only=True)
    member3 = StudentSerializer(many=False,read_only=True)
    member4 = StudentSerializer(many=False,read_only=True)
    mentor = TeacherSerializer(many=False, read_only=True)

    class Meta:
        model = Project
        exclude = ('associated_files', 'proposal')


class ProjectDetailProposalSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    mentor = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
