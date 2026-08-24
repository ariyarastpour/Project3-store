from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "last_name", "email","phone_number", "description")

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'hireUsFormFirstName',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'hireUsFormLasttName',
                'placeholder': 'نام خانوادگی'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'hireUsFormWorkEmail',
                'placeholder': 'email@site.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'hireUsFormPhone',
                'placeholder': '+9891200000'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'id': 'hireUsFormDetails',
                'placeholder': 'توضیحات خود را وارد نمایید',
                'rows': 5
            })
        }