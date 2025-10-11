# saluni_kiume/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import MaleSalon, MaleBooking, MaleService, MaleStylist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# ---------------------------
# List all male salons
# ---------------------------
def male_salon_list(request):
    salons = MaleSalon.objects.all()
    return render(request, 'saluni_kiume/male_salon_list.html', {'salons': salons})

# ---------------------------
# Male salon detail
# ---------------------------
def male_salon_detail(request, salon_id):
    salon = get_object_or_404(MaleSalon, id=salon_id)
    services = salon.services.filter(active=True)
    stylists = salon.stylists.filter(is_active=True)
    return render(request, 'saluni_kiume/male_salon_detail.html', {
        'salon': salon,
        'services': services,
        'stylists': stylists
    })

# ---------------------------
# Male salon services JSON (optional)
# ---------------------------
def male_salon_list_json(request):
    salons = MaleSalon.objects.all()
    data = [
        {
            'id': s.id,
            'name': s.name,
            'address': s.address,
            'phone': s.phone,
            'email': s.email,
        } for s in salons
    ]
    return JsonResponse(data, safe=False)

# ---------------------------
# Create booking (male salon)
# ---------------------------
@login_required
def create_male_booking(request, salon_id):
    salon = get_object_or_404(MaleSalon, id=salon_id)
    services = salon.services.filter(active=True)
    stylists = salon.stylists.filter(is_active=True)

    if request.method == 'POST':
        service_id = request.POST.get('service')
        stylist_id = request.POST.get('stylist')
        start = request.POST.get('start_datetime')
        service = get_object_or_404(MaleService, id=service_id)
        stylist = get_object_or_404(MaleStylist, id=stylist_id)

        booking = MaleBooking.objects.create(
            customer=request.user,
            salon=salon,
            service=service,
            stylist=stylist,
            start_datetime=start,
            end_datetime=None  # auto-calculated in model
        )
        return redirect('kiume:male_booking_detail', booking_id=booking.id)

    return render(request, 'saluni_kiume/create_male_booking.html', {
        'salon': salon,
        'services': services,
        'stylists': stylists
    })

# ---------------------------
# Male booking detail
# ---------------------------
@login_required
def male_booking_detail(request, booking_id):
    booking = get_object_or_404(MaleBooking, id=booking_id)
    return render(request, 'saluni_kiume/male_booking_detail.html', {'booking': booking})
