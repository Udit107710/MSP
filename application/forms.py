from django import forms
from .models import Project
from student.models import Student


class ProjectForm(forms.ModelForm):
    member1 = forms.ModelChoiceField(Student.objects.filter(lock=0))
    # member2 = forms.ModelChoiceField(Student.objects.filter(lock=0),required=False)
    # member3 = forms.ModelChoiceField(Student.objects.filter(lock=0),required=False)
    # member4 = forms.ModelChoiceField(Student.objects.filter(lock=0),required=False)
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['member2','member3','member4']
