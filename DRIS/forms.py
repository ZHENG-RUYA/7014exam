# DRIS/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, DisasterReport, AidRequest, Shelter, Volunteer

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['address']


class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = DisasterReport
        fields = ['disaster_type', 'location', 'gps_coordinates', 'severity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class DisasterReportFilterForm(forms.Form):
    disaster_type = forms.ChoiceField(
        choices=DisasterReport.DisasterType.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    severity = forms.ChoiceField(
        choices=DisasterReport.SeverityLevel.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'})
    )


class AidRequestForm(forms.ModelForm):
    class Meta:
        model = AidRequest
        fields = ['disaster', 'aid_type', 'description']
        widgets = {
            'disaster': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = '__all__'
        widgets = {
            'facilities': forms.Textarea(attrs={'rows': 4}),
        }


class VolunteerRegisterForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['skills', 'certification', 'experience']
        widgets = {
            'certification': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 3}),
        }


class VolunteerUpdateForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['skills', 'availability', 'certification', 'experience']
        widgets = {
            'certification': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 3}),
        }