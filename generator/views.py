from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LawForm, Gaussian, Laplace, Alpha, Gamma, SimulationForm
from .libs import white_noise, loperator, lspline
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

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

            n = float(form.cleaned_data['n'])
            s.set_lambda(n)

            T = float(form.cleaned_data['T'])
            h = float(form.cleaned_data['h'])

            DATA = []
            numsim = int(form.cleaned_data['numsim'])

            s.sample(T)
            grid, dt = s.get_grid_samples(T, h, show=False)

            plt.style.use('seaborn-poster')
            fig, ax = plt.subplots()

            ax.step(grid, dt, where='post', lw = 1.5)
            canvas = FigureCanvasAgg(fig)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            response = HttpResponse(buf.getvalue(), content_type='image/png')
            return response

    else:
        form = SimulationForm()
    print(law_name, params)
    return render(request, 'generator/simulationinput.html', {'form':form})
