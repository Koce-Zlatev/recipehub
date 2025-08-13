from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio']
        widgets = {
            'display_name': forms.TextInput(attrs={'placeholder': 'Как да се показва името ви'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Кратко представяне…'}),
        }
