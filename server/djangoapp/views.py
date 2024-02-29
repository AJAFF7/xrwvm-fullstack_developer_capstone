
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CarMake, CarModel

# Create your views here.

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data.get('userName', '')
    password = data.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

def logout_user(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        return JsonResponse({"username": username})
    else:
        return JsonResponse({"error": "User is not logged in"}, status=401)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data.get('userName', '')
    password = data.get('password', '')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)
    else:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

def get_cars(request):
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
    return JsonResponse({"CarModels": cars})







# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...




# from django.http import JsonResponse
# from django.contrib.auth import login, authenticate, logout
# import logging
# import json
# from django.views.decorators.csrf import csrf_exempt

# # Get an instance of a logger
# logger = logging.getLogger(__name__)

# # Create your views here.

# # Create a `login_request` view to handle sign in request
# @csrf_exempt
# def login_user(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data['userName']
#         password = data['password']
#         user = authenticate(username=username, password=password)
#         response_data = {"userName": username}
#         if user is not None:
#             login(request, user)
#             response_data["status"] = "Authenticated"
#         return JsonResponse(response_data)
#     elif request.method == 'GET':
#         # Logout the user if it's a GET request
#         if request.user.is_authenticated:
#             username = request.user.username
#             logout(request)
#             return JsonResponse({"userName": username, "status": "Logged out"})
#         else:
#             return JsonResponse({"status": "error", "message": "User is not logged in"}, status=400)
#     else:
#         return JsonResponse({"status": "error", "message": "Only POST and GET requests are allowed"}, status=405)
