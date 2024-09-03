from django.shortcuts import render
from dod_api.api_hooks import get_request_data, get_request_hotel_data
from django.templatetags.static import static
from django.utils import translation
from django.shortcuts import redirect



def set_language(request):
    user_language = request.GET.get('language', 'en')
    translation.activate(user_language)
    request.session['language'] = user_language
    return render(request, 'base.html')




def home(request):
    city_data = get_request_data('get_all_city')
    blogs_data = get_request_data('get_blogs')
    context = {
        'city_data': city_data if city_data else [],
        'blogs_data': blogs_data if blogs_data else []
    }
    return render(request, 'base.html', context)



def get_hotel_by_city(request, property_city, property_city_id):
    default_url = static('img/default-product.png')  # Use the static file
    hotel_data = get_request_hotel_data('get_hotel_detail', property_city_id)
    
    hotels = []
    if hotel_data:
        for hotel in hotel_data.get('hotels', []):
            if hotel.get('files'):
                hotel['first_file_url'] = hotel['files'][0]['Url']
            else:
                hotel['first_file_url'] = default_url

            hotels.append(hotel)
    
    context = {
        'property_city': property_city,
        'hotel_list_data': {'hotels': hotels, 'hotel_count':len(hotels)},
    }
    return render(request, 'hotel_listing_page.html', context)



