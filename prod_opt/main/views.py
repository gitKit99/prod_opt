from django.shortcuts import render, redirect
from .models import Task
from .models import Component
from .models import ComponentCost
from .models import ComponentLimit
from .models import Bottle
from .forms import TaskForm
from django.template.defaulttags import register
import numpy as np
from scipy.optimize import minimize


g_n = 0
g_m = 0

g_a = []
g_p = []
g_c = []
g_q_tilda = []
g_q = []
g_b = []


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

    global g_n
    global g_m
    global g_a
    global g_p
    global g_c
    global g_q_tilda
    global g_q
    global g_b
    g_n = len(list(components))
    g_m = len(list(bottles))

    bottle_i = 0
    comp_i = 0
    g_a.clear()
    g_a = [None] * g_n
    g_a[bottle_i] = []
    for comp_cost in component_costs:
        g_a[bottle_i].append(comp_cost.cost)
        comp_i = comp_i + 1
        if (comp_i >= g_n):
            comp_i = 0
            bottle_i = bottle_i + 1
            g_a[bottle_i] = []

    g_q.clear()
    g_q_tilda.clear()
    for comp in components:
        g_q.append(comp.q0)
        g_q_tilda.append(comp.q1)

    g_c.clear()
    g_p.clear()
    for i, bottle in enumerate(bottles):
        g_c.append(bottle.cost)
        mult_sum = 0
        for j, el in enumerate(g_a[i]):
            mult_sum += el * g_q[j]
        g_p.append(2 * (mult_sum + g_c[i]))

    g_b.clear()
    for limit in component_limits:
        g_b.append(limit.limit)

    costs = []
    for i in range(len(components)):
        inner = list(ComponentCost.objects.filter(component=i+1).order_by('id'))
        costs.append(inner)
    return render(request, 'main/calculate.html', {'components': list(components), 'comp_costs': list(component_costs),
                                               'comp_limits': list(component_limits), 'bottles': list(bottles),
                                                   'costs': list(costs)})


def result(request):
    x_bounds = []
    for bottle in Bottle.objects.all():
        x_bounds.append(bottle.xMin)
        x_bounds.append(bottle.xMax)
    bounds = tuple(x_bounds)

    y_bounds = []
    for comp in Component.objects.all():
        x_bounds.append(comp.yMin)
        x_bounds.append(comp.yMax)
    bounds += tuple(y_bounds)

    v_bounds = []
    for comp in Component.objects.all():
        x_bounds.append(comp.vMin)
        x_bounds.append(comp.vMax)
    bounds += tuple(v_bounds)

    w_bounds = []
    for comp in Component.objects.all():
        x_bounds.append(comp.wMin)
        x_bounds.append(comp.wMax)
    bounds += tuple(w_bounds)

    con1 = {'type': 'eq', 'func': constraint1}
    con2 = {'type': 'eq', 'func': constraint2}
    cons = [con1, con2]

    global g_n
    global g_m
    args0 = np.zeros(g_n + 3 * g_m)
    sol = minimize(objective, args0, method='SLSQP', bounds=bounds, constraints=cons)
    x = sol[:g_n]
    y = sol[g_n:g_n + g_m]
    v = sol[g_n + 2 * g_m: g_n + 3 * g_m]
    w = sol[g_n + g_m: g_n + 2 * g_m]
    return render(request, 'main/result.html', {'x': x, 'y': y, 'v': v, 'w': w})


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_at_index(li, i):
    return li[i]


def objective(args, sign=-1):
    global g_n
    global g_m
    global g_p
    global g_c
    global g_q_tilda
    global g_q
    x = args[:g_n]
    y = args[g_n:g_n + g_m]
    w = args[g_n + g_m: g_n + 2 * g_m]
    #p = args[g_n + 3 * g_m: 2 * g_n + 3 * g_n]
    #c = args[2 * g_n + 3 * g_m: 3 * g_n + 3 * g_n]
    #q_tilda = args[3 * g_n + 3 * g_m: 3 * g_n + 4 * g_n]
    #q = args[3 * g_n + 4 * g_m: 3 * g_n + 5 * g_n]
    return sign * (np.sum((g_p - g_c) * x) + np.sum(g_q_tilda * w) - np.sum(g_q * y))


def constraint1(args):
    global g_n
    global g_m
    global g_a
    x = args[:g_n]
    #y = args[g_n:g_n + g_m]
    outer_sum = 0.
    for i in range(g_m):
        inner_sum = 0.
        for j in range(g_n):
            inner_sum += g_a[j][i] * x[i]
        outer_sum += inner_sum
    return outer_sum


def constraint2(args):
    global g_n
    global g_m
    global g_b
    x = args[:g_n]
    y = args[g_n:g_n + g_m]
    w = args[g_n + g_m: g_n + 2 * g_m]
    v = args[g_n + 2 * g_m: g_n + 3 * g_m]
    return np.sum(g_b + v - y - w)


# def x_constraint(x_min, x, x_max):
#     for x_el in x:
#         if x_el < x_min or x_el > x_max:
#             return False
#     return True
#
#
# def y_constraint(y_min, y, y_max):
#     for y_el in y:
#         if y_el < y_min or y_el > y_max:
#             return False
#     return True
#
#
# def v_constraint(v_min, v, v_max):
#     for v_el in v:
#         if v_el < v_min or v_el > v_max:
#             return False
#     return True
#
#
# def w_constraint(w_min, w, w_max):
#     for w_el in w:
#         if w_el < w_min or w_el > w_max:
#             return False
#     return True
