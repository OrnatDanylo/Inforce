from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', login_view, name='login'),
    path('router/', include(router.urls)),

    path('current_day_menu/', get_current_day_menu_view, name='current_day_menu'),
    path('results_for_current_day/', get_results_for_current_day_view, name='results_for_current_day'),

    path('register_employee/', employee_registration_view, name='register_employee'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('employee/home/', employee_home, name='employee-home'),
    path('company/home/', company_home, name='company-home'),

    path('restaurant/create/', create_restaurant, name='create_restaurant'),
    path('restaurants/<int:restaurant_id>/upload_menu/', upload_menu, name='upload_menu'),
    path('restaurants/upload_menu/<int:menu_id>/', upload_menu_put, name='upload_menu_put'),
    
]