from django import forms
from .models import Law


LAWS = [
    ('gaussian', 'Gaussian'),
    ('laplace', 'Laplace'),
    ('gamma', 'Gamma'),
    ('alpha_stable', 'Alpha Stable')
]

class LawForm(forms.Form):
    law_name = forms.ChoiceField(choices=LAWS, widget=forms.RadioSelect(), initial="gaussian")

class Gaussian(forms.Form):
    variance = forms.FloatField(min_value=0, initial=1)

class Alpha(forms.Form):
    alpha = forms.FloatField(min_value=0, max_value=2, initial=1)

class Laplace(forms.Form):
    scale = forms.FloatField(min_value=0, initial=1)

class Gamma(forms.Form):
    shape = forms.FloatField(min_value=0, initial=1)
    scale = forms.FloatField(min_value=0, initial=1)

class SimulationForm(forms.Form):
    p = forms.CharField(label="P",initial="1, 0")
    q = forms.CharField(label="Q", initial="1")
    T = forms.FloatField(min_value=0, label="Simulation interval T", initial=1)
    h = forms.FloatField(min_value=0, label="Step size h", initial=0.01)
    numsim = forms.IntegerField(min_value=1, max_value=10000, label="Number of simulations")
