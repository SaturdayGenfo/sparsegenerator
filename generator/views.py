from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LawForm, Gaussian, Laplace, Alpha, Gamma

def law_select(request):
    if request.method == "POST":
        form = LawForm(request.POST)
        if form.is_valid():
            return redirect('param_select', law_name=form.cleaned_data['law_name'])
    else:
        form = LawForm()
    return render(request, 'generator/lawinput.html', {'form' : form})

def param_select(request, law_name='gaussian'):
    laws = {'gaussian': Gaussian,'alpha_stable': Alpha,'laplace': Laplace,'gamma' : Gamma}
    if request.method == "POST":
        return HttpResponse("ZOOP")
    else:
        form = laws[law_name]
    return render(request, 'generator/paraminput.html', {'law':law_name, 'form':form})
