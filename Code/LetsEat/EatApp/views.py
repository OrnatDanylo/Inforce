from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from .models import Company, Restaurant, Menu, Employee, Vote, User
from .serializers import CompanySerializer, RestaurantSerializer, MenuSerializer, EmployeeSerializer, VoteSerializer, EmployeeRegistrationSerializer
from .services import get_current_day_menu, get_results_for_current_day

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

@api_view(['GET'])
def get_current_day_menu_view(request):
    menu = get_current_day_menu()
    if menu is not None:
        serializer = MenuSerializer(menu)
        return Response(serializer.data)
    else:
        # Handle the case where the menu for the current day is not available
        return Response({"message": "Menu not available for the current day"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_results_for_current_day_view(request):
    results = get_results_for_current_day()
    return Response(results)

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