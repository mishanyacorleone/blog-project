from django import forms
import re


class GradeForm(forms.Form):
    student_name = forms.CharField(max_length=100, label="Имя студента", widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=100, label="Предмет", widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.IntegerField(min_value=2, max_value=5, label="Оценка", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_student_name(self):
        name = self.cleaned_data['student_name']
        if not re.match(r'^[А-Яа-яA-Za-zёЁ\s-]+$', name):
            raise forms.ValidationError("Имя должно содержать только буквы.")
        return name

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if not re.match(r'^[А-Яа-яA-Za-zёЁ\s-]+$', subject):
            raise forms.ValidationError("Название предмета должно содержать только буквы.")
        return subject


class UploadXMLForm(forms.Form):
    file = forms.FileField(label='Выберите XML файл', widget=forms.FileInput(attrs={'class': 'form-control'}))