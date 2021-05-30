import math

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
    g_n = len(list(bottles))
    g_m = len(list(components))

    g_a.clear()
    g_a = []
    for j in range(g_n):
        inner = []
        for i in range(g_m):
            inner.append(component_costs[j * g_m + i].cost)
        g_a.append(inner)

    g_q.clear()
    g_q_tilda.clear()
    for comp in components:
        g_q.append(comp.q0)
        g_q_tilda.append(comp.q1)

    g_c.clear()
    g_p.clear()
    for i, bottle in enumerate(bottles):
        g_c.append(bottle.cost)
        mult_sum = 0.
        for j, el in enumerate(g_a[i]):
            mult_sum += el * g_q[j]
        g_p.append(2. * (mult_sum + g_c[i]))

    g_b.clear()
    for limit in component_limits:
        g_b.append(limit.limit)

    print("g_p size: " + str(len(g_p)))
    print("g_c size: " + str(len(g_c)))
    print("g_q size: " + str(len(g_q)))
    print("g_q_tilda size: " + str(len(g_q_tilda)))
    costs = []
    for i in range(len(components)):
        inner = list(ComponentCost.objects.filter(component=i + 1).order_by('id'))
        costs.append(inner)
    return render(request, 'main/calculate.html', {'components': list(components), 'comp_costs': list(component_costs),
                                                   'comp_limits': list(component_limits), 'bottles': list(bottles),
                                                   'costs': list(costs)})


def constraint1(args):
    global g_n
    global g_m
    global g_a
    global g_b
    res = []
    x = args[:g_n]
    y = args[g_n: g_n + g_m]
    for i in range(g_m):
        inner_sum = 0.
        for j in range(g_n):
            inner_sum += g_a[j][i] * x[j]
        inner_sum -= y[i]
        res.append(inner_sum)
    return res


def calculate_reminder(args):
    global g_m
    global g_n
    global g_a
    global g_b
    y = args[g_n: g_n + g_m]
    w = args[g_n + g_m: g_n + 2 * g_m]
    v = args[g_n + 2 * g_m: g_n + 3 * g_m]
    new_b = []
    for i in range(g_m):
        new_b.append(g_b[i] + v[i] - y[i] - w[i])
    return new_b


def constraint2(args):
    global g_n
    global g_m
    global g_b
    y = args[g_n:g_n + g_m]
    w = args[g_n + g_m: g_n + 2 * g_m]
    v = args[g_n + 2 * g_m: g_n + 3 * g_m]
    res = []
    for i in range(g_m):
        res.append(g_b[i] + v[i] - y[i] - w[i])
    return res


def save_result(z, x, v, w, new_b):
    print('got: z = ' + str(z))
    print(x)


def result(request):
    x_bounds = []
    bounds = ()
    for bottle in Bottle.objects.all():
        inner_tuple = (float(bottle.xMin), float(bottle.xMax))
        x_bounds.append(inner_tuple)
    bounds = tuple(x_bounds)

    y_bounds = []
    for comp in Component.objects.all():
        inner_tuple = (comp.yMin, comp.yMax)
        y_bounds.append(inner_tuple)
    bounds += tuple(y_bounds)

    w_bounds = []
    for comp in Component.objects.all():
        inner_tuple = (comp.wMin, comp.wMax)
        w_bounds.append(inner_tuple)
    bounds += tuple(w_bounds)

    v_bounds = []
    for comp in Component.objects.all():
        inner_tuple = (comp.vMin, comp.vMax)
        v_bounds.append(inner_tuple)
    bounds += tuple(v_bounds)

    con1 = {'type': 'eq', 'fun': constraint1}
    con2 = {'type': 'eq', 'fun': constraint2}
    cons = [con1, con2]

    global g_n
    global g_m
    args0 = np.zeros(g_n + 3 * g_m, dtype=float)
    print("Length of bounds: " + str(len(bounds)))
    # print(g_b)
    sol = minimize(objective, args0, method='SLSQP', bounds=bounds, constraints=cons, tol=1.e-5)
    print(sol)
    print("constraint1: " + str(constraint1(sol.x)))
    print("constraint2: " + str(constraint2(sol.x)))
    args = sol.x
    for x_index in range(g_n):
        args[x_index] = int(args[x_index])
    x = args[: g_n]
    for i in range(g_m):
        inner_sum = 0.
        for j in range(g_n):
            inner_sum += g_a[j][i] * x[j]
        args[g_n + i] = inner_sum
    y = args[g_n:g_n + g_m]
    v = args[g_n + 2 * g_m: g_n + 3 * g_m]
    w = args[g_n + g_m: g_n + 2 * g_m]
    reminder = calculate_reminder(args)
    return render(request, 'main/result.html',
                  {'z': -sol.fun, 'message': sol.message, 'success': sol.success, 'x': x, 'y': y, 'v': v, 'w': w,
                   'rem': reminder})


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
    sum1 = 0.
    for j in range(g_n):
        sum1 += (g_p[j] - g_c[j]) * x[j]
    sum2 = 0.
    sum3 = 0.
    for i in range(g_m):
        sum2 += g_q[i] * w[i]
        sum3 += g_q[i] * y[i]
    return sign * (sum1 + sum2 - sum3)
