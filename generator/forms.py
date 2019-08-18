from django import forms
from .models import Law


LAWS = [
    ('gaussian', 'Gaussian'),
    ('laplace', 'Laplace'),
    ('gamma', 'Gamma'),
    ('alpha_stable', 'Alpha Stable')
]

class LawForm(forms.Form):
    law_name = forms.ChoiceField(choices=LAWS, widget=forms.RadioSelect())

class Gaussian(forms.Form):
    variance = forms.FloatField(min_value=0)

class Alpha(forms.Form):
    alpha = forms.FloatField(min_value=0, max_value=2)

class Laplace(forms.Form):
    scale = forms.FloatField(min_value=0)

class Gamma(forms.Form):
    shape = forms.FloatField(min_value=0)
    scale = forms.FloatField(min_value=0)

class SimulationForm(forms.Form):
    operator = forms.CharField()
    n = forms.IntegerField(min_value=1)
    T = forms.FloatField(min_value=0)
    h = forms.FloatField(min_value=0)
