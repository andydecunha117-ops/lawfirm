from django.shortcuts import render, get_object_or_404, redirect
from .models import Lawyer, Slot, Appointment
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils.dateparse import parse_date
from django.db.models import F, ExpressionWrapper, DurationField

def home(request):
    return render(request, 'booking/home.html')

def lawyers(request):
    category = request.GET.get("category")  

    
    if category and category != "all":
        lawyers_list = Lawyer.objects.filter(category__name=category)
    else:
        lawyers_list = Lawyer.objects.all()

   
    categories = Lawyer.objects.values_list("category__name", flat=True).distinct()

    
    data = []
    for lawyer in lawyers_list:
        first_slot = lawyer.slot_set.filter(booked=False).first()
        data.append({
            "lawyer": lawyer,
            "first_slot": first_slot,
        })

    return render(request, "booking/lawyer.html", {
        "data": data,
        "categories": categories,
        "selected_category": category,
    })


    return render(request, "booking/lawyer.html", {"data": data})

@login_required
def book(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)

    if request.method == "POST":
        Appointment.objects.create(
            client=request.user,
            lawyer=slot.lawyer,
            slot=slot,
            fee_charged=slot.lawyer.fee
        )
        slot.booked = True
        slot.save()
        return redirect("booking_success")

    return render(request, 'booking/book.html', {"slot": slot})

def booking_success(request):
    return render(request, "booking/booking_success.html")

def reports(request):
    result = None

    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")

        start_date = parse_date(start)
        end_date = parse_date(end)

        
        appointments = Appointment.objects.filter(
            created__range=(start_date, end_date)
        )

        # 1. Number of consultations completed
        consultations = appointments.filter(status="completed").count()

        # 2A. Revenue per lawyer
        revenue = appointments.values(
            "lawyer__user__username"
        ).annotate(
            total_revenue=Sum("fee_charged")
        )

        # 2B. Total consultation hours per lawyer
        durations = appointments.annotate(
            duration=ExpressionWrapper(
                F("slot__end") - F("slot__start"),
                output_field=DurationField()
            )
        ).values(
            "lawyer__user__username"
        ).annotate(
            total_hours=Sum("duration")
        )

        # 3. Distribution by category
        distribution = appointments.values(
            "lawyer__category__name"
        ).annotate(
            total=Count("id")
        )

        # 3B. Distribution by lawyer
        distribution_lawyer = appointments.values(
            "lawyer__user__username"
        ).annotate(
            total=Count("id")
        )


        
        result = {
            "consultations": consultations,
            "revenue": revenue,
            "hours": durations,
            "distribution": distribution,
            "distribution_lawyer": distribution_lawyer,

        }

    return render(request, "booking/reports.html", {"result": result})



def slots_by_date(request):
    slots = None

    if request.method == "POST":
        selected_date = request.POST.get("date")
        date_obj = parse_date(selected_date)

        slots = Slot.objects.filter(
            start__date=date_obj,
            booked=False
        ).order_by("start")

    return render(request, "booking/slots_by_date.html", {"slots": slots})

def make_booking(request):
    lawyers = Lawyer.objects.all()
    slots = None
    selected_lawyer = None
    selected_month = None

    if request.method == "POST":
        lawyer_id = request.POST.get("lawyer")
        month_str = request.POST.get("month")  

        
        slot_id = request.POST.get("slot")
        if slot_id:
            slot = Slot.objects.get(id=slot_id)
            Appointment.objects.create(
                client=request.user,
                lawyer=slot.lawyer,
                slot=slot,
                fee_charged=slot.lawyer.fee
            )
            slot.booked = True
            slot.save()
            return redirect("booking_success")

        
        selected_lawyer = lawyer_id
        selected_month = month_str

        if lawyer_id and month_str:
            year, month = map(int, month_str.split("-"))

            slots = Slot.objects.filter(
                lawyer_id=lawyer_id,
                start__year=year,
                start__month=month,
                booked=False
            ).order_by("start")

    return render(request, "booking/make_booking.html", {
        "lawyers": lawyers,
        "slots": slots,
        "selected_lawyer": selected_lawyer,
        "selected_month": selected_month,
    })


@login_required
def my_appointments(request):
    
    lawyer = Lawyer.objects.get(user=request.user)
    appts = Appointment.objects.filter(lawyer=lawyer)

    if request.method == "POST":
        appt_id = request.POST.get("appt_id")
        status = request.POST.get("status")
        notes = request.POST.get("notes")

        appt = Appointment.objects.get(id=appt_id)
        appt.status = status
        appt.notes = notes
        appt.save()

    return render(request, "booking/my_appointments.html", {"appointments": appts})

