from django.shortcuts import render, redirect
from .models import Task
from .models import Component
from .models import ComponentCost
from .models import ComponentLimit
from .models import Bottle
from .forms import TaskForm
from django.template.defaulttags import register


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Form was incorrect'

    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)


def calculate(request):
    components = Component.objects.all()
    component_costs = ComponentCost.objects.all()
    component_limits = ComponentLimit.objects.all()
    bottles = Bottle.objects.all()
    costs = []
    for i in range(len(components)):
        inner = list(ComponentCost.objects.filter(component=i+1).order_by('id'))
        costs.append(inner)
    return render(request, 'main/calculate.html', {'components': list(components), 'comp_costs': list(component_costs),
                                               'comp_limits': list(component_limits), 'bottles': list(bottles),
                                                   'costs': list(costs)})


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_at_index(li, i):
    return li[i]
