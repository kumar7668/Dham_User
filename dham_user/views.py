from django.shortcuts import render
import requests
from dod_api.api_hooks import get_request_data, get_hotel_list_ViaId, get_blog_detail_via_id
from django.templatetags.static import static
from django.utils import translation
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpResponseNotFound






def set_language(request):
    user_language = request.GET.get('language', 'en')
    translation.activate(user_language)
    request.session['language'] = user_language
    return render(request, 'base.html')




# Utility function for formatting dates
def format_datetime(date_str):
    """Format a given datetime string into 'Month Day, Year' format."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date_obj.strftime('%b %d, %Y')
    except ValueError:
        return date_str  # Fallback if the date format is invalid

def home(request):
    city_data = get_request_data('get_all_city')
    kanha_jiki_nagri_data = get_request_data('kanha_jiki_nagri')
    upcoming_tours_events_data = get_request_data('upcoming_tours_events')
    top_destinations_data = get_request_data('top_destinations')
    blogs_data = get_request_data('recent_blogs')

    # Process blogs_data
    if blogs_data and 'updatedBlogs' in blogs_data:
        for blog in blogs_data['updatedBlogs']:
            blog['first_file_url'] = blog['files'][0].get('Url', None) if blog.get('files') and blog['files'] else None
            blog['formatted_date'] = format_datetime(blog['createdAt']) if blog.get('createdAt') else None
    else:
        blogs_data = {'updatedBlogs': []}

    # Process kanha_jiki_nagri_data (CityTours)
    if kanha_jiki_nagri_data and 'CityTours' in kanha_jiki_nagri_data:
        for city_tour in kanha_jiki_nagri_data['CityTours']:
            city_tour['formatted_start_from'] = format_datetime(city_tour.get('start_from'))
            city_tour['formatted_end_at'] = format_datetime(city_tour.get('end_at'))
    
    # Process upcoming_tours_events_data (Events)
    if upcoming_tours_events_data and 'upcommingToursAndEvent' in upcoming_tours_events_data:
        for upcoming_tours in upcoming_tours_events_data['upcommingToursAndEvent']:
            upcoming_tours['formatted_start_from'] = format_datetime(upcoming_tours.get('start_from'))
            upcoming_tours['formatted_end_at'] = format_datetime(upcoming_tours.get('end_at'))
   
    # Process top_destinations_data (Destinations)
    if top_destinations_data and 'TopDestinations' in top_destinations_data:
        for top_destinations in top_destinations_data['TopDestinations']:
            top_destinations['formatted_start_from'] = format_datetime(top_destinations.get('start_from'))
            top_destinations['formatted_end_at'] = format_datetime(top_destinations.get('end_at'))

    context = {
        'blogs_data': blogs_data,
        'kanha_jiki_nagri': kanha_jiki_nagri_data,
        'city_data': city_data,
        'upcoming_tours_events_data': upcoming_tours_events_data,
        'top_destinations_data': top_destinations_data,
    }
    return render(request, 'base.html', context)


def accommodation_state(request):
    context={
        'data':'Data',
    }
    return render(request, 'accommodation_state.html', context)

def guide(request):
    context={
        'data':'Data',
    }
    return render(request, 'guide/guide_base.html', context)

def guide_carousel(request):
    context={
        'data':'Data',
    }
    return render(request, 'guide/guide_carousel.html', context)

def guide_detail(request):
    context={
        'data':'Data',
    }
    return render(request, 'guide/guide_detail_page.html', context)

def live_darshan(request):
    context={
        'data':'Data',
    }
    return render(request, 'live_darshan/live_base.html', context)

def e_pooja(request):
    context={
        'data':'Data',
    }
    return render(request, 'e_pooja.html', context)

def e_pooja_detail(request):
    context={
        'data':'Data',
    }
    return render(request, 'e-puja/e_puja_detail.html', context)

def live_darshan_detail(request):
    context={
        'data':'Data',
    }
    return render(request, 'live_darshan/live_darshan_detail.html', context)

def contact_us(request):
    context={
        'data':'Data',
    }
    return render(request, 'skeleton/contact_us.html', context)

def about_us(request):
    context={
        'data':'Data',
    }
    return render(request, 'skeleton/about_us.html', context)

def privacy_policy(request):
    context={
        'data':'Data',
    }
    return render(request, 'skeleton/privacy_policy.html', context)

def terms_condition(request):
    context={
        'data':'Data',
    }
    return render(request, 'skeleton/terms_condition.html', context)

def faq_board(request):
    context={
        'data':'Data',
    }
    return render(request, 'skeleton/faq_board.html', context)

def testimonials(request):
    context={
        'data':'Data',
    }
    return render(request, 'skeleton/testimonials.html', context)




def blog_list(request):
    # Fetch the recent blogs from API or another data source
    blogs_data = get_request_data('recent_blogs')
    
    # Ensure blogs_data is valid and contains blogs
    if blogs_data and 'updatedBlogs' in blogs_data:
        for blog in blogs_data['updatedBlogs']:
            # Try to get the first file URL, or set to None if unavailable
            if blog.get('files') and len(blog['files']) > 0:
                blog['first_file_url'] = blog['files'][0].get('Url', None)
            else:
                blog['first_file_url'] = None
            # Format the 'createdAt' date
            if blog.get('createdAt'):
                try:
                    created_at_dt = datetime.strptime(blog['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    blog['formatted_date'] = created_at_dt.strftime('%d')
                    if 4 <= int(blog['formatted_date']) <= 20 or 24 <= int(blog['formatted_date']) <= 30:
                        blog['formatted_date'] += 'th'
                    else:
                        blog['formatted_date'] += {1: 'st', 2: 'nd', 3: 'rd'}.get(int(blog['formatted_date']) % 10, 'th')
                
                    blog['formatted_date'] += created_at_dt.strftime(' %b %Y')
                except ValueError:
                    blog['formatted_date'] = blog['createdAt']  # Fallback in case of a formatting error
    else:
        # Ensure blogs_data is an empty list if the API response is invalid
        blogs_data = {'updatedBlogs': []}

    context = {
        'blogs_data': blogs_data,
    }
    # Render the template with the context
    return render(request, 'blogs/blog_list_base.html', context)



def blog_detail_page(request, blog_loc, blog_id):
    try:
        default_url = settings.STATIC_URL + 'img/default-product.png'
        # Fetch blog details using the provided blog_id
        get_blog_via_id = get_blog_detail_via_id('get_blog_by_id', blog_id)
        if get_blog_via_id and 'data' in get_blog_via_id and get_blog_via_id['data'].get('files'):
            # Fetch the first file's URL if available
            get_blog_via_id['data']['first_file_url'] = get_blog_via_id['data']['files'][0].get("Url", default_url)
        else:
            get_blog_via_id['data']['first_file_url'] = default_url

        context = {
            'blog_data': get_blog_via_id,
            'blog_loc': blog_loc
        }

    except (KeyError, IndexError, TypeError):
        # Fallback to default blog data in case of any error
        context = {
            'blog_data': None,
            'blog_loc': blog_loc
        }
    return render(request, 'blogs/blog_detail_page.html', context)



from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings

def get_hotel_by_city(request, property_city, property_city_id):
    default_url = settings.STATIC_URL + 'img/default-product.png'  # Use the static file

    # Get selected filters from GET parameters
    selected_amenities = request.GET.getlist('amenities[]')  # Handles multiple amenities
    selected_property_types = request.GET.getlist('propertyTypes[]')  # Handles multiple property types
    selected_selectPrice = request.GET.getlist('selectPrice[]')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Prepare filters for the hotel API, removing invalid values (None or empty)
    filters = {}
    
    # Handling amenities filter
    if selected_amenities:
        valid_amenities = [amenity for amenity in selected_amenities if amenity]
        if valid_amenities:
            filters['amenities'] = selected_amenities 
    # Handling property types filter
    if selected_property_types:
        valid_property_types = [ptype for ptype in selected_property_types if ptype]
        if valid_property_types:
            filters['propertyTypeId'] = selected_property_types 
    
    # Handling select price range
    if selected_selectPrice:
        valid_selectPrice = [price for price in selected_selectPrice if price]
        if valid_selectPrice:
            converted_list = [int(num) for price_range in valid_selectPrice for num in price_range.split(' to ')]
            checked_price_range = set(converted_list)
            min_checked = min(checked_price_range)
            max_checked = max(checked_price_range)
            filters['priceRange'] = f'{min_checked} to {max_checked}'

    # Handling min and max price
    if min_price and min_price.isdigit():
        filters['min_price'] = min_price
    
    if max_price and max_price.isdigit():
        filters['max_price'] = max_price

    # Fetch hotel data using the filters
    try:
        hotel_data = get_hotel_list_ViaId('get_hotel_list', property_city_id, filters)
    except Exception as e:
        print(f"Error fetching hotel data: {e}")
        hotel_data = None

    # Process hotel data
    hotels = []
    if hotel_data:
        for hotel in hotel_data.get('hotels', []):
            if hotel.get('files'):
                hotel['first_file_url'] = hotel['files'][0].get('Url', default_url)
            else:
                hotel['first_file_url'] = default_url
            hotels.append(hotel)

    # Fetch amenities and property types
    try:
        amenities_data = get_request_data('get_amenities')
    except Exception as e:
        print(f"Error fetching amenities data: {e}")
        amenities_data = []

    try:
        property_types_data = get_request_data('get_property_types')
    except Exception as e:
        print(f"Error fetching property types data: {e}")
        property_types_data = []

    # Process price range counts
    formattedPriceRangeCounts = []
    if hotel_data and hotel_data.get('priceRangeCounts'):
        for price_range, count in hotel_data['priceRangeCounts'].items():
            try:
                min_price, max_price = price_range.split(' to ')
                formatted_price_range = f"₹ {min_price} - ₹ {max_price}"
                id= f"{min_price}_{max_price}"
                formattedPriceRangeCounts.append({
                    'display': formatted_price_range,
                    'value': price_range,
                    'count': count,
                    'id':id
                })
            except ValueError:
                print(f"Unexpected price range format: {price_range}")
                continue

    # Return a JSON response if an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'hotels': hotels, 'hotel_count': len(hotels)})

    # Render the template for a normal request
    context = {
        'property_city': property_city,
        'priceRangeCounts': hotel_data.get('priceRangeCounts') if hotel_data and hotel_data.get('priceRangeCounts') else [],
        'hotel_list_data': {'hotels': hotels, 'hotel_count': len(hotels)},
        'amenities': amenities_data,
        'property_types': property_types_data,
        'selected_amenities': selected_amenities,
        'selected_property_types': selected_property_types,
        'formattedPriceRangeCounts': formattedPriceRangeCounts
    }
    return render(request, 'hotel_listing_page.html', context)
