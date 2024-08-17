from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label='Введите населенный пункт',
                           max_length=100)
