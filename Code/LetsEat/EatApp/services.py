from datetime import date
from .models import Menu, Vote

def get_current_day_menu():
    today = date.today()
    try:
        menu = Menu.objects.get(date=today)
    except Menu.DoesNotExist:
        # Handle the case where the menu for the current day is not available
        menu = None
    return menu

def get_results_for_current_day():
    today = date.today()
    votes = Vote.objects.filter(date=today)
    # Implement logic to calculate the results from the votes
    # For example, counting votes per menu item and returning the winner(s)
    results = {}
    return results
