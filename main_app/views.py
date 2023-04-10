from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Creature, Toy
from .forms import FeedingForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def creatures_index(request):
    creatures = Creature.objects.all()
    return render(request, 'creatures/index.html', {'creatures': creatures})

def creature_detail(request, creature_id):
    creature = Creature.objects.get(id=creature_id)
    feeding_form = FeedingForm()

    creature_toys_ids = creature.toys.all().values_list('id')
    toys_creature_doesnt_have = Toy.objects.exclude(id__in=creature_toys_ids)

    return render(request, 'creatures/detail.html', {
        'creature': creature,
        'feeding_form': feeding_form,
        'toys': toys_creature_doesnt_have,
        })

def add_feeding(request, creature_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.creature_id = creature_id
        new_feeding.save()
    return redirect('creature_detail', creature_id=creature_id)

def assoc_toy(request, creature_id, toy_id):
    creature = Creature.objects.get(id=creature_id)
    creature.toys.add(toy_id)
    return redirect('creature_detail', creature_id=creature_id)

def unassoc_toy(request, creature_id, toy_id):
    creature = Creature.objects.get(id=creature_id)
    creature.toys.remove(toy_id)
    return redirect('creature_detail', creature_id=creature_id)

class CreatureCreate(CreateView):
    model = Creature
    fields = ('name', 'species', 'description', 'age')
    template_name = 'creatures/creature_form.html'

class CreatureUpdate(UpdateView):
    model = Creature
    fields = ('name', 'species', 'description', 'age')
    template_name = 'creatures/creature_form.html'

class CreatureDelete(DeleteView):
    model = Creature
    success_url = '/creatures/'
    template_name = 'creatures/creature_confirm_delete.html'



class ToyList(ListView):
    model = Toy
    template_name = 'toys/toy_list.html'

class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/toy_detail.html'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyUpdate(UpdateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/toy_confirm_delete.html'