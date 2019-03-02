from django import forms

class tag_search_form(forms.Form):
    tag_name = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={ "placeholder" : "Enter text"}))