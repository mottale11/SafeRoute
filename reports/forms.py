from django import forms
from .models import IncidentReport, IncidentImage, SavedZone


class IncidentReportForm(forms.ModelForm):
    """Form for submitting incident reports"""
    class Meta:
        model = IncidentReport
        fields = ['title', 'category', 'description', 'severity', 'latitude', 'longitude', 
                  'location_name', 'incident_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of the incident'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 
                                                'placeholder': 'Provide detailed description of what happened'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'id': 'id_latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'id': 'id_longitude'}),
            'location_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Street name, landmark'}),
            'incident_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['incident_date'].required = True


class IncidentImageForm(forms.ModelForm):
    """Form for uploading incident images"""
    class Meta:
        model = IncidentImage
        fields = ['image', 'image_type', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional description'}),
        }


class SavedZoneForm(forms.ModelForm):
    """Form for saving risk zones"""
    class Meta:
        model = SavedZone
        fields = ['name', 'latitude', 'longitude', 'radius']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'radius': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1', 'max': '10'}),
        }

