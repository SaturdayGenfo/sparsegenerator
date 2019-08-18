from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LawForm, Gaussian, Laplace, Alpha, Gamma, SimulationForm

LAWS = {
    'gaussian' :  'Gaussian',
    'laplace': 'Laplace',
    'gamma': 'Gamma',
    'alpha_stable': 'Alpha Stable'
}

def law_select(request):
    if request.method == "POST":
        form = LawForm(request.POST)
        if form.is_valid():
            return redirect('param_select', law_name=form.cleaned_data['law_name'])
    else:
        form = LawForm()
    return render(request, 'generator/lawinput.html', {'form' : form})

def param_select(request, law_name):
    laws = {'gaussian': Gaussian,'alpha_stable': Alpha,'laplace': Laplace,'gamma' : Gamma}
    if request.method == "POST":
        form = laws[law_name](request.POST)
        if form.is_valid():
            params = list(form.cleaned_data.values())
            return redirect('simu', law_name=law_name, params=params)
    else:
        form = laws[law_name]
    return render(request, 'generator/paraminput.html', {'law':LAWS[law_name], 'form':form})

def simu(request, law_name, params):
    form = SimulationForm()
    return render(request, 'generator/simulationinput.html', {'form':form})
