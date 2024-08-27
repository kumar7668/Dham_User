from django.shortcuts import render
from dod_api.api_hooks import get_api_data

# Create your views here.
def home(request):
    # Call the utility function with the appropriate key
    city_data = get_api_data('get_all_city')
    # Pass the data to the template context
    context = {
        'city_data': city_data if city_data else []  # Ensure it's not None
    }
    return render(request, 'base.html', context)

    # return render(request, 'base.html')




def fetch_city_data(request):
    # Call the utility function with the appropriate key
    city_data = get_api_data('get_all_city')

    # Pass the data to the template context
    context = {
        'city_data': city_data if city_data else []  # Ensure it's not None
    }

    # Render the template with the city data
    return render(request, 'near_by_home.html', context)
