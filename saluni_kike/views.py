# saluni_kike/views.py
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Salon, Service, Stylist, AvailabilitySlot, Booking, Payment, Review

# List all salons
def salon_list(request):
    salons = Salon.objects.all()
    return render(request, 'saluni_kike/salon_list.html', {'salons': salons})

# Detail for a single salon
def salon_detail(request, salon_id):
    salon = get_object_or_404(Salon, pk=salon_id)
    services = salon.services.all()
    return render(request, 'saluni_kike/salon_detail.html', {'salon': salon, 'services': services})

# JSON version (optional)
def salon_list_json(request):
    salons = list(Salon.objects.values())
    return JsonResponse(salons, safe=False)

# Create booking (simple POST example)
def create_booking(request):
    if request.method == 'POST':
        salon_id = request.POST.get('salon')
        service_id = request.POST.get('service')
        # … retrieve other POST fields …
        salon = get_object_or_404(Salon, pk=salon_id)
        service = get_object_or_404(Service, pk=service_id)
        booking = Booking.objects.create(
            customer=request.user,
            salon=salon,
            service=service,
            start_datetime=request.POST.get('start_datetime'),
            end_datetime=request.POST.get('end_datetime'),
            status='pending'
        )
        return HttpResponseRedirect('/bookings/')  # or success page
    else:
        salons = Salon.objects.all()
        return render(request, 'saluni_kike/create_booking.html', {'salons': salons})




    # saluni_kike/views.py
from django.shortcuts import render, redirect
from .forms import SalonForm

def salon_register(request):
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            salon = form.save()  # saluni mpya
            # unaweza kumpeleka user dashboard au hatua inayofuata
            return redirect('salon_list')  # badilisha kulingana na url yako
    else:
        form = SalonForm()
    return render(request, 'saluni_kike/salon_register.html', {'form': form})


# saluni_kike/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Salon
from .forms import SalonProfileForm

def salon_update_profile(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    if request.method == 'POST':
        form = SalonProfileForm(request.POST, instance=salon)
        if form.is_valid():
            form.save()
            return redirect('salon_list')  # au profile page
    else:
        form = SalonProfileForm(instance=salon)

    return render(request, 'saluni_kike/update_profile.html', {'form': form})



