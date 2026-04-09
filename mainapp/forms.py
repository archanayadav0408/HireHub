from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = "__all__"
        widgets = {
            "name" : forms.TextInput(attrs={"class": "form-control custom-input"}),
            "email" : forms.EmailInput(attrs={"class": "form-control custom-input"}),
            "contact" : forms.NumberInput(attrs={"class": "form-control custom-input"}),
            "subject" : forms.TextInput(attrs={"class": "form-control custom-input"}),
            "message" : forms.Textarea(attrs={"class": "form-control custom-textArea","rows":"2"}),
        }