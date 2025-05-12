from django import forms
from django.contrib.auth import get_user_model
from .models import Question, Reply
from taggit.forms import TagWidget

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    email    = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("Passwords must match.")
        return data
    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body','tags']  # Fields to be filled by the user
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter question details'}),
            'tags': TagWidget(attrs={'class': 'form-control','placeholder': 'Add tags separated by commas'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your reply here...',
                'rows': 1
            }),
        }