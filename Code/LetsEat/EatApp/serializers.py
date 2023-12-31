from rest_framework import serializers
from .models import Company, Restaurant, Menu, Employee, Vote, User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['username', 'email', 'password', 'name', 'surname']

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password']
        }
        user = User.objects.create_user(**user_data)
        employee_data = {
            'user': user,
            'name': validated_data['name'],
            'surname': validated_data['surname']
        }
        employee = Employee.objects.create(**employee_data)
        return employee
    
class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        exclude = ('company',)

    def create(self, validated_data):
        company = self.context.get('company')
        restaurant = Restaurant.objects.create(company=company, **validated_data)
        return restaurant    
    

class UploadManuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ('restaurant',)

    def create(self, validated_data):
        restaurant = self.context.get('restaurant')
        menu = Menu.objects.create(restaurant=restaurant, **validated_data)
        return menu        