from django import forms
from .models import Pet
from .models import AdoptionDemand

from django.forms import ModelForm

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'pet_type', 'breed', 'age', 'gender', 'size',
            'description', 'story', 'location', 'adoption_fee', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'story': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class PetFilterForm(forms.Form):
    pet_type = forms.ChoiceField(
        choices=[('', 'All')] + Pet.PET_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    gender = forms.ChoiceField(
        choices=[('', 'Any')] + Pet.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    size = forms.ChoiceField(
        choices=[('', 'Any')] + Pet.SIZE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min age'})
    )
    max_age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max age'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    max_fee = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max fee'})
    )


class AdoptionDemandForm(forms.ModelForm):
    class Meta:
        model = AdoptionDemand
        fields = [
            'experience',
            'past_ownership',
            'living_arrangement',
            'motivation_letter',
        ]
        # ── ADD WIDGETS FOR THOSE FIELDS ───────────────────────────────────────────
        widgets = {
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'past_ownership': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'living_arrangement': forms.TextInput(attrs={'class': 'form-control'}),
            'motivation_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        # ────────────────────────────────────────────────────────────────────────────
