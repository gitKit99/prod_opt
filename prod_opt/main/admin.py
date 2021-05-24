from django.contrib import admin
from .models import Task
from .models import Component
from .models import ComponentCost
from .models import ComponentLimit
from .models import Bottle


admin.site.register(Task)
admin.site.register(Component)
admin.site.register(ComponentCost)
admin.site.register(ComponentLimit)
admin.site.register(Bottle)


