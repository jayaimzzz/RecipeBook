from django import forms
from recipebook.models import Recipe, Author


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=15)
    instructions = forms.CharField(widget=forms.Textarea)

