from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from .forms import PetFilterForm, AdoptionDemandForm, PetForm
from .models import Pet, AdoptionDemand


def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin)  # ← ADDED THIS LINE
def dashboard(request):
    all_pets = Pet.objects.all().order_by('-posted_date')
    all_requests = AdoptionDemand.objects.all().select_related('user', 'pet').order_by('-requested_at')
    return render(request, 'pets/dashboard.html', {
        'all_pets': all_pets,
        'all_requests': all_requests,
    })


@login_required
@user_passes_test(is_admin)
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.posted_by = request.user
            pet.save()
            messages.success(request, 'Pet added successfully!')
            return redirect('dashboard')
    else:
        form = PetForm()
    return render(request, 'pets/add_pet.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet updated successfully!')
            return redirect('dashboard')
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})


@login_required
@user_passes_test(is_admin)
def manage_adoption(request, demand_id):
    demand = get_object_or_404(AdoptionDemand, id=demand_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['APPROVED', 'REJECTED']:
            demand.status = new_status
            demand.approved_by = request.user
            demand.decided_at = timezone.now()
            demand.save()

            if new_status == 'APPROVED':
                demand.pet.is_adopted = True
                demand.pet.adopted_by = demand.user
                demand.pet.save()

            messages.success(request, f'Adoption request {new_status.lower()}')
            return redirect('dashboard')
    return render(request, 'pets/manage_adoption.html', {'demand': demand})


def home(request):
    pets = Pet.objects.all().order_by('-posted_date')
    form = PetFilterForm(request.GET)
    if form.is_valid():
        pet_type = form.cleaned_data.get('pet_type')
        gender = form.cleaned_data.get('gender')
        size = form.cleaned_data.get('size')
        min_age = form.cleaned_data.get('min_age')
        max_age = form.cleaned_data.get('max_age')
        max_fee = form.cleaned_data.get('max_fee')

        if pet_type:
            pets = pets.filter(pet_type=pet_type)
        if gender:
            pets = pets.filter(gender=gender)
        if size:
            pets = pets.filter(size=size)
        if min_age is not None:
            pets = pets.filter(age__gte=min_age)
        if max_age is not None:
            pets = pets.filter(age__lte=max_age)
        if max_fee is not None:
            pets = pets.filter(adoption_fee__lte=max_fee)

    paginator = Paginator(pets, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pets/home.html', {
        'pets': page_obj,
        'form': form,
        'is_paginated': pets.count() > 6,
        'page_obj': page_obj,
    })


def pet_details(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={request.path}")

    demand_submitted = False
    if request.user.is_authenticated:
        demand_submitted = AdoptionDemand.objects.filter(
            user=request.user, pet=pet
        ).exists()

    form = AdoptionDemandForm(request.POST or None)

    if request.method == 'POST' and request.user.is_authenticated and not demand_submitted and form.is_valid():
        demand = AdoptionDemand.objects.create(
            user=request.user,
            pet=pet,
            status='PENDING',
            experience=form.cleaned_data['experience'],
            past_ownership=form.cleaned_data['past_ownership'],
            living_arrangement=form.cleaned_data['living_arrangement'],
            motivation_letter=form.cleaned_data['motivation_letter']
        )
        demand_submitted = True
        messages.success(request, "Thank you! Your adoption request has been received and will be reviewed shortly.")
    
    return render(request, 'pets/pet_details.html', {
        'pet': pet,
        'form': form,
        'demand_submitted': demand_submitted,
    })