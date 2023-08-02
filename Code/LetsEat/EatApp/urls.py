from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet, RestaurantViewSet, MenuViewSet, EmployeeViewSet, VoteViewSet, get_current_day_menu_view, get_results_for_current_day_view, employee_registration_view

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('current_day_menu/', get_current_day_menu_view, name='current_day_menu'),
    path('results_for_current_day/', get_results_for_current_day_view, name='results_for_current_day'),
    path('register_employee/', employee_registration_view, name='register_employee'),
]