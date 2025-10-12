# saluni_kike/views.py

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from .models import Salon, Service, Stylist, AvailabilitySlot, Booking, Payment, Review
from .forms import SalonForm, SalonProfileForm, BookingForm

# Get the custom user model
Customer = get_user_model()


# ---------------------------
# Salon views
# ---------------------------

def salon_list(request):
    salons = Salon.objects.all()
    return render(request, 'saluni_kike/salon_list.html', {'salons': salons})


def salon_detail(request, salon_id):
    salon = get_object_or_404(Salon, pk=salon_id)
    services = salon.services.all()
    return render(request, 'saluni_kike/salon_detail.html', {'salon': salon, 'services': services})


def salon_list_json(request):
    salons = list(Salon.objects.values())
    return JsonResponse(salons, safe=False)


def salon_register(request):
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kike:salon_list')
    else:
        form = SalonForm()
    return render(request, 'saluni_kike/salon_register.html', {'form': form})


def salon_update_profile(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    if request.method == 'POST':
        form = SalonProfileForm(request.POST, instance=salon)
        if form.is_valid():
            form.save()
            return redirect('salon_list')
    else:
        form = SalonProfileForm(instance=salon)
    return render(request, 'saluni_kike/update_profile.html', {'form': form})


def salon_stylists(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    stylists = salon.stylists.filter(is_active=True)
    return render(request, 'saluni_kike/salon_stylists.html', {'salon': salon, 'stylists': stylists})


# ---------------------------
# Booking views
# ---------------------------

@login_required
def create_booking(request, salon_id=None):
    """
    If salon_id is provided, create booking for a specific salon.
    If not, handle generic booking POST.
    """
    customer = request.user  # dynamic Customer

    if salon_id:
        salon = get_object_or_404(Salon, id=salon_id)
    else:
        salon = None

    if request.method == 'POST':
        salon_id_post = request.POST.get('salon')
        service_id = request.POST.get('service')
        salon = get_object_or_404(Salon, pk=salon_id_post)
        service = get_object_or_404(Service, pk=service_id)

        booking = Booking.objects.create(
            customer=customer,
            salon=salon,
            service=service,
            start_datetime=request.POST.get('start_datetime'),
            end_datetime=request.POST.get('end_datetime'),
            status='pending'
        )
        return HttpResponseRedirect('/bookings/')  # or a success page
    else:
        form = BookingForm(salon=salon)
        salons = Salon.objects.all()
        return render(request, 'saluni_kike/create_booking.html', {
            'salons': salons,
            'form': form,
            'salon': salon,
        })


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'saluni_kike/booking_detail.html', {'booking': booking})


# ---------------------------
# User authentication
# ---------------------------

def user_login(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Pass 'username=phone' because backend uses it
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Karibu, {user.get_full_name() or user.phone}!")
            next_url = request.GET.get('next') or 'kike:salon_list'
            return redirect(next_url)
        else:
            messages.error(request, "Nambari ya simu au nenosiri si sahihi.")

    return render(request, 'saluni_kike/login.html')



def user_logout(request):
    logout(request)
    messages.success(request, "Umetoka kwenye akaunti yako.")
    return redirect('kike:login')
