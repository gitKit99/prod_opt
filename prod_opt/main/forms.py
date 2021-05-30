from .models import Bottle, Component, ComponentCost
from django.forms import ModelForm, TextInput, Select


class BottleForm(ModelForm):
    class Meta:
        model = Bottle
        fields = ["name", "cost", "xMin", "xMax"]
        widgets = {"name": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Input name'
        }),
            "cost": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Input cost'}),
            "xMin": TextInput(attrs={
                'class': 'form-control',
                'initial': '0'}),
            "xMax": TextInput(attrs={
                'class': 'form-control',
                'initial': '0'})

        }


class InForm(ModelForm):
    class Meta:
        model = Component
        fields = ["name", "yMin", "yMax", "vMin", "vMax", "wMin", "wMax"]
        widgets = {"name": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Input name'
        }),
            "yMin": TextInput(attrs={
                'class': 'form-control',
                'initial': '0'}),
            "yMax": TextInput(attrs={
                'class': 'form-control',
                'initial': '100'}),
            "vMin": TextInput(attrs={
                'class': 'form-control',
                'initial': '0'}),
            "vMax": TextInput(attrs={
                'class': 'form-control',
                'initial': '100'}),
            "wMin": TextInput(attrs={
                'class': 'form-control',
                'initial': '0'}),
            "wMax": TextInput(attrs={
                'class': 'form-control',
                'initial': '100'}),

        }


class CompForm(ModelForm):
    class Meta:
        model = ComponentCost
        fields = ["component", "bottle", "cost", ]
        widgets = {"component": Select(attrs={
            'class': 'form-control',
        }),
            "bottle": Select(attrs={
                'class': 'form-control',
            }),
            "cost": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Input cost'})}


