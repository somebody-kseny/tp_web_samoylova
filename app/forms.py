from django import forms
from .models import Question, Answer, Author
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']
    tags = forms.CharField()
    tags.label='Tags'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

class AuthorForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
    def clean_username(self):
        cd = self.cleaned_data
        if Author.objects.filter(user__username = cd['username']).exists():
            raise forms.ValidationError('Такое имя пользователя уже занято')
        return cd['username']
    def clean_email(self):
        cd = self.cleaned_data
        if Author.objects.filter(user__email = cd['email']).exists():
            raise forms.ValidationError('Такой e-mail уже зарегестрирован')
        return cd['email']

class EditAuthorForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']