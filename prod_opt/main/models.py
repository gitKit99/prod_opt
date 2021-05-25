from django.db import models


class Task(models.Model):
    title = models.CharField('Title', max_length=50)
    task = models.TextField('Description')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class Component(models.Model):
    name = models.CharField('Name', max_length=50)
    yMin = models.FloatField('ymin', default=0.0)
    yMax = models.FloatField('ymax', default=100.0)
    vMin = models.FloatField('vmin', default=0.0)
    vMax = models.FloatField('vmax', default=100.0)
    wMin = models.FloatField('wmin', default=0.0)
    wMax = models.FloatField('wmax', default=100.0)
    q0 = models.FloatField('q', default=0.0)
    q1 = models.FloatField('^q', default=0.0)

    def __str__(self):
        return self.name


class Bottle(models.Model):
    cost = models.FloatField('c')
    name = models.CharField('Name', max_length=50)
    xMin = models.IntegerField('xmin', default=0)
    xMax = models.IntegerField('xmax', default=0)

    def __str__(self):
        return self.name + " - " + str(self.cost)


class ComponentCost(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    bottle = models.ForeignKey(Bottle, on_delete=models.CASCADE)
    cost = models.FloatField('a')

    def __str__(self):
        return str(self.component) + " - " + str(self.bottle) + " - " + str(self.cost)


class ComponentLimit(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    limit = models.FloatField('b')

    def __str__(self):
        return str(self.component) + " - " + str(self.limit)
