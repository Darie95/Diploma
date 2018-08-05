from django.core.exceptions import ValidationError
from django.forms import EmailField, CharField, ModelForm, DateInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Quiz.models import Comments
import datetime


class SearchForm(forms.Form):
    search = forms.CharField(label='Название или категория квиза')


class UserCreationForm(UserCreationForm):
    email = EmailField(label="Email_address", required=True,
                       help_text="Обязательно")
    code_word = CharField(label="Code_word", required=True,
                          help_text="Обязательно")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "code_word")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.code_word = self.cleaned_data["code_word"]
        if commit:
            user.save()
        return user


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comments_text']


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comments_text']


class FilterForm(forms.Form):
    min_date=forms.DateField(label = 'С', widget= forms.DateInput(attrs={'class':'datepicker'}))
    max_date=forms.DateField(label = 'По', widget= forms.DateInput(attrs={'class':'datepicker'}))


