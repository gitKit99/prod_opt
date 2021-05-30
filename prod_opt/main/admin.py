from django.contrib import admin
from .models import Task
from .models import Component
from .models import ComponentCost
from .models import ComponentLimit
from .models import Bottle
from .models import Result
from .models import X
from .models import V
from .models import W


admin.site.register(Task)
admin.site.register(Component)
admin.site.register(ComponentCost)
admin.site.register(ComponentLimit)
admin.site.register(Bottle)
admin.site.register(Result)
admin.site.register(X)
admin.site.register(V)
admin.site.register(W)


