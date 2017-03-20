from django import forms

class searchForm(forms.Form):
    searchquery = forms.CharField(label='q', max_length=50)
