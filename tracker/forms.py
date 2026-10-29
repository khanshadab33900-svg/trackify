from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Project, Ticket, Comment

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg rounded-3'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'role':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control form-control-lg rounded-3',
                    'placeholder': f"Enter {self.fields[field].label.lower()}"
                })

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-3',
                'placeholder': 'e.g. NextGen Web Portal, Android App v2'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 4,
                'placeholder': 'Provide detailed overview and scope of this software project...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'project', 'screenshot']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-3',
                'placeholder': 'Brief summary of the issue (e.g. Button unclickable on Safari)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 5,
                'placeholder': 'Steps to reproduce the bug, expected behavior, and error messages...'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'project': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'screenshot': forms.FileInput(attrs={
                'class': 'form-control rounded-3'
            }),
        }

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'status', 'assigned_developer']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-3'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 4
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'assigned_developer': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_developer'].queryset = User.objects.filter(role='developer')
        self.fields['assigned_developer'].empty_label = "Select Assigned Developer"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 3,
                'placeholder': 'Add updates, logs, or debugging notes...'
            }),
        }
