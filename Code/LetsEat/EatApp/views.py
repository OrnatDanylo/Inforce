from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Company, Restaurant, Menu, Employee, Vote, User
from .serializers import *
from .services import get_current_day_menu, get_results_for_current_day
from datetime import date

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        # Implement logic to handle employee authentication using DRF's authentication classes
        # ...
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@login_required
@api_view(['GET'])
def get_current_day_menu_view(request):
    menu = Menu.objects.filter(date=date.today())
    existing_restaurant_ids = [m.restaurant.id for m in menu]
    restaurants = Restaurant.objects.exclude(id__in=existing_restaurant_ids)
    if menu is not None or restaurants is not None:
        return render(request, 'menu/today_menu.html', {'restaurants':restaurants, 'menu':menu})
    else:
        # Handle the case where the menu for the current day is not available
        return Response({"message": "Menu not available for the current day"}, status=status.HTTP_404_NOT_FOUND)

@login_required
@api_view(['GET'])
def get_results_for_current_day_view(request):
    menu = Menu.objects.filter(date=date.today()).order_by('-rate')
    if menu is not None:
        return render(request, 'menu/today_menu_rating.html', {'menu':menu})
    else:
        # Handle the case where the menu for the current day is not available
        return Response({"message": "Menu not available for the current day"}, status=status.HTTP_404_NOT_FOUND)

#registration section
@api_view(['GET', 'POST'])
def employee_registration_view(request):
    if request.method == 'POST':
        print(request.data)
        serializer = EmployeeRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:
        return render(request, 'employee/register_employee.html')

#login section    
class MyTokenObtainPairView(TokenObtainPairView):
    pass    

def login_view(request):
    return render(request, 'authentication/login.html')

@api_view(['GET','POST'])
def login_view(request):
    if request.method == 'POST':
        
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is None:
            return Response({"error": "Invalid username or password."}, status=400)
        #login
        login(request, user)

        request.session['username'] = request.data['username']

        if Employee.objects.filter(user__username=request.data['username']).exists():
            print(request)
            return redirect('employee/home/')
        elif Company.objects.filter(owner__username=request.data['username']).exists():
            print(request)
            return redirect('company/home/')  
        else:    
            return Response({"error": "Invalid user."}, status=400)
    else:
        return render(request, 'authentication/login.html')

#home screen
@login_required
@api_view(['GET'])
def company_home(request):
    username = request.session.get('username', '')
    try:
        company =  Company.objects.filter(owner__username = username).first()
        restaurants = Restaurant.objects.filter(company=company)
    except Company.DoesNotExist:
        company = None
        restaurants = []
    
    context = {
        'company': company,
        'restaurants': restaurants,
    }
    return render(request, 'company/com_home.html', context)   


@login_required
@api_view(['GET','POST'])
def create_restaurant(request):
    if request.method == 'POST':
        print(request.data)
        company =  Company.objects.filter(owner__username = request.session.get('username', '')).first()
        serializer = CreateRestaurantSerializer(data=request.data, context={'company': company})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:
        return render(request, 'restaurant/create_restaurant.html')
    
@login_required    
@api_view(['GET','POST'])
def upload_menu(request, restaurant_id):
    if request.method == 'POST':
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        serializer = UploadManuSerializer(data=request.data, context={'restaurant': restaurant})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:    
        return render(request, 'menu/upload_menu.html', {'restaurant_id':restaurant_id})
    
@login_required    
@api_view(['POST','PUT'])
def upload_menu_put(request, menu_id):
    try:
        menu = Menu.objects.get(pk=menu_id)

        # Increase the menu rating
        menu.rate += 1
        menu.save()

        return Response({'message': 'Rating increased successfully.'}, status=status.HTTP_200_OK)

    except Menu.DoesNotExist:
        return Response({'error': 'Menu not found.'}, status=status.HTTP_404_NOT_FOUND)


    
@login_required
@api_view(['GET'])
def employee_home(request):
    username = request.session.get('username', '')
    return render(request, 'employee/emp_home.html')   
        