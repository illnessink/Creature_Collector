from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Creature, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'creaturecollector'


# Create your views here.

@login_required
def add_photo(request, creature_id):
    # attempt to collect photo submission from request
    photo_file = request.FILES.get('photo-file', None)
    # if photo file present
    if photo_file:
        # setup an s3 client object - obj w/methods for working with s3
        s3 = boto3.client('s3')
        # create a unique name for the photo file
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # try to upload file to aws s3
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # generate unique url for the image
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # save the url as a new instance of the photo model
            # make sure we associate the cat with the photo model instance
            Photo.objects.create(url=url, creature_id=creature_id)
        # if theres an error (exception)
        except Exception as error:
            # print error message for debugging
            print('photo upload failed')
            print('error')
    # redirect to the detail page regardless if successful
    return redirect('creature_detail', creature_id=creature_id)


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def creatures_index(request):
    creatures = Creature.objects.filter(user=request.user)
    return render(request, 'creatures/index.html', {'creatures': creatures})

@login_required
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

@login_required
def add_feeding(request, creature_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.creature_id = creature_id
        new_feeding.save()
    return redirect('creature_detail', creature_id=creature_id)

@login_required
def assoc_toy(request, creature_id, toy_id):
    creature = Creature.objects.get(id=creature_id)
    creature.toys.add(toy_id)
    return redirect('creature_detail', creature_id=creature_id)

@login_required
def unassoc_toy(request, creature_id, toy_id):
    creature = Creature.objects.get(id=creature_id)
    creature.toys.remove(toy_id)
    return redirect('creature_detail', creature_id=creature_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('creatures_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error': error_message})

class CreatureCreate(LoginRequiredMixin, CreateView):
    model = Creature
    fields = ('name', 'species', 'description', 'age')
    template_name = 'creatures/creature_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreatureUpdate(LoginRequiredMixin, UpdateView):
    model = Creature
    fields = ('name', 'species', 'description', 'age')
    template_name = 'creatures/creature_form.html'

class CreatureDelete(LoginRequiredMixin, DeleteView):
    model = Creature
    success_url = '/creatures/'
    template_name = 'creatures/creature_confirm_delete.html'



class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/toy_list.html'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/toy_detail.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/toy_confirm_delete.html'