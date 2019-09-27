from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LawForm, Gaussian, Laplace, Alpha, Gamma, SimulationForm
from .libs import white_noise, loperator, lspline
import matplotlib.pyplot as plt
import numpy as np
import os


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
    if request.method == "POST":
        form = SimulationForm(request.POST)
        if form.is_valid():
            params = params[1:-1].split(',')
            w = white_noise.white_noise(law_name, list(map(float, params)))
            P = list(map(float, form.cleaned_data['p'].split(',')))
            Q = list(map(float, form.cleaned_data['q'].split(',')))

            L = loperator.Operator(P, Q)
            s = lspline.L_spline(L, w)




            T = float(form.cleaned_data['T'])
            h = float(form.cleaned_data['h'])

            s.set_lambda(np.ceil(1/h)*5)

            DATA = []
            numsim = int(form.cleaned_data['numsim'])

            for _ in range(numsim):
                s.sample(T)
                grid, dt = s.get_grid_samples(T, h, show=False)
                DATA.append(dt)
            dir = os.path.join("generator", "static")
            np.savetxt(os.path.join(dir , "data.csv"), DATA)


            plt.style.use('seaborn-poster')

            plt.step(grid, dt, where='post', lw = 1.5)
            plt.savefig(os.path.join(dir, "fig.png"), format='png')

            return redirect('download')

    else:
        form = SimulationForm()
    print(law_name, params)
    return render(request, 'generator/simulationinput.html', {'form':form})

def download(request):
    return render(request, 'generator/download.html')
