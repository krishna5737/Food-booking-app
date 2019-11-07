from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Hotels, Booking, City
from datetime import datetime, timedelta
# Create your views here.
def login_page(request):
    if not request.user.is_anonymous:
        return redirect(reverse("home"))
    return render(request, "login.html")

@login_required(login_url="/auth/login")
def home(request):
    avail_hotels, full_hotels = [], []
    clean_bookings()
    hotels = Hotels.objects.all()
    city =  City.objects.all()
    currentCity = request.GET.get("city","")
    if(currentCity):
        for hotel in hotels:
            if(str(hotel.city)==currentCity):
                if hotel.is_hotel_full() or len(Booking.objects.filter(user=request.user,hotel_name=hotel)) == 6:
                    full_hotels.append(hotel)
                else:
                    avail_hotels.append(hotel)
    else:
        for hotel in hotels:
            if hotel.is_hotel_full() or len(Booking.objects.filter(user=request.user,hotel_name=hotel)) == 6:
                full_hotels.append(hotel)
            else:
                avail_hotels.append(hotel)


    return render(request, "home.html",{
        "hotels":avail_hotels,
        "full_hotels": full_hotels,
        "city": city,
    })

def auth_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("home"))
    return redirect(reverse("login"))


def create_account(request):
    if request.method == "POST":
        username = request.POST["create_username"]
        password = request.POST["create_password"]
        if len(User.objects.filter(username=username)) == 0:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
    return redirect(reverse("login"))

@login_required(login_url="/auth/login")
def book_table(request):
    if request.method=="POST":
        clean_bookings()
        hotel_name = request.POST["hotelname"]
        hotel = Hotels.objects.get(name=hotel_name)
        bookings = Booking.objects.filter(user=request.user,hotel_name=hotel)
        if len(bookings) < 6 and not hotel.is_hotel_full():
            Booking.objects.create(hotel_name=hotel,user=request.user)
    return redirect(reverse("home"))


def clean_bookings():
    threshold = datetime.now() - timedelta(hours=24)
    bookings = Booking.objects.filter(time__lt=threshold)
    bookings.delete()


