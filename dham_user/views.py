from django.shortcuts import render, redirect
import requests
from dod_api.api_hooks import userRegistration, verifyOtp, userLogin, get_request_data, get_hotel_list_ViaId, get_blog_detail_via_id, get_hotel_detail_ViaId, post_booking_detail, get_guides_list, get_guides_by_Id
from dod_api.forms.userForms import LoginForm, RegisterForm, BaseOtpForm
from django.templatetags.static import static
from django.utils import translation
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpResponseNotFound
import json  
from django.contrib.auth import logout
from django.urls import reverse


# Register view
def register_view(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            fname = register_form.cleaned_data['firstname']
            lname = register_form.cleaned_data['lastname']
            email = register_form.cleaned_data['email']
            phone = register_form.cleaned_data['phone']

            try:
                # Call userRegistration to register the user
                register_response = userRegistration(fname, lname, email, phone)

                if register_response.status_code == 201:
                    request.session['user_mobile'] = phone
                    request.session['user_email'] = email
                    return JsonResponse({'status': 'success', 'message': 'Registration successful! Please check your OTP.'}, status=201)

                elif register_response.status_code == 400:
                    response_content = register_response.content.decode('utf-8')
                    json_data = json.loads(response_content)  # Correctly parse the JSON response

                    error_message = json_data.get('error', {}).get('message', '')

                    if error_message == 'User with Entered Mobile Number is already exists':
                        return JsonResponse({'status': 'error', 'message': error_message}, status=400)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Registration failed. Please try again.'}, status=400)

                else:
                    return JsonResponse({'status': 'error', 'message': 'Registration failed. Please try again.'}, status=register_response.status_code)

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Error occurred during registration: {str(e)}'}, status=500)

        else:
            return JsonResponse({'status': 'error', 'message': register_form.errors.as_json()}, status=400)

    # GET request handling
    return render(request, 'base.html', {
        'register_form': register_form,
        'otp_form': None,
        'login_form': None,
        'otp_step': None
    })


# OTP verification view
def verify_otp_view(request):
    try:
        otp_form = BaseOtpForm()

        if request.method == 'POST':
            otp_form = BaseOtpForm(request.POST)
            otp_from_type = request.POST.get('form_type')

            if otp_form.is_valid():
                otp = otp_form.cleaned_data['otp']
                mobile = request.session.get('user_mobile')  # Get phone from session

                try:
                    # Call your OTP verification API
                    verify_register_otp = verifyOtp(mobile, otp)

                    # Check if OTP verification was successful
                    if verify_register_otp.status_code == 200:
                        response_content = verify_register_otp.content.decode('utf-8')
                        json_data = json.loads(response_content)

                        # Store token in session
                        request.session['token'] = json_data['data']['token']
                        
                        # Create a response object
                        response = JsonResponse({
                            'status': 'success',
                            'message': 'OTP verified successfully! Redirecting to My Account...' 
                            if otp_from_type == 'login-otp-form' 
                            else 'Profile verified successfully! Redirecting to Login...'
                        }, status=200)
                        
                        # Set the cookie in the response object
                        response.set_cookie('user', json_data['data']['customer']['_id'])

                        # Set session values
                        request.session['user_authenticated'] = True 
                        request.session['user_id'] = json_data['data']['customer']['_id']
                        request.session['user_email'] = json_data['data']['customer']['email']
                        request.session['user_mobile'] = json_data['data']['customer']['mobile']
            

                        # Return the response with the cookie set
                        return response
                    else:
                        return JsonResponse({
                            'status': 'error', 
                            'message': 'Invalid OTP or verification failed. Please try again.'
                        }, status=400)
                except Exception as e:
                    return JsonResponse({
                        'status': 'error', 
                        'message': f'Error during OTP verification: {str(e)}'
                    }, status=500)
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': otp_form.errors.as_json()
                }, status=400)

        return render(request, 'base.html', {
            'register_form': None,
            'otp_form': otp_form,
            'login_form': None,
            'otp_step': 'register'  # OTP step for registration
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': f'Error in OTP verification: {str(e)}'
        }, status=500)


def login_view(request):
    # Log out the user if they are a superuser
    if request.user.is_superuser:
        logout(request)

    try:
        login_form = LoginForm()

        if request.method == 'POST':
            login_form = LoginForm(request.POST)

            if login_form.is_valid():
                phone = login_form.cleaned_data['phone']
                # otp = login_form.cleaned_data['otp']  # Assuming OTP is also submitted via the form

                try:
                    # # Retrieve the token from the session
                    # token = request.session.get('token')

                    # Call external or custom userLogin function to validate phone + OTP
                    user_login = userLogin(phone)

                    # Check if the OTP login was successful
                    if user_login.status_code == 200:
                        request.session['user_mobile'] = phone
                        return JsonResponse({'status': 'success', 'message': 'Verify OTP for Login'}, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid OTP or verification failed. Please try again.'}, status=400)
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f'Error during login: {str(e)}'}, status=500)
            else:
                    return JsonResponse({'status': 'error', 'message': 'Phone number mismatch. Please check the phone number.'}, status=400)
           

        return render(request, 'base.html', {
            'register_form': None,
            'otp_form': None,
            'login_form': login_form,
            'otp_step': None
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error occurred during login: {str(e)}'}, status=500)


def dham_logout_view(request):
    if request.method == 'POST':
        # Clear only necessary session data
       # Keep token for next login
        request.session['user_authenticated'] = False  # Mark user as logged out
        logout(request)  # This logs out the user if using Django's authentication system

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

















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
    # insta_reels_temp =
    city_data = get_request_data('get_all_city')
    kanha_jiki_nagri_data = get_request_data('kanha_jiki_nagri')
    upcoming_tours_events_data = get_request_data('upcoming_tours_events')
    top_destinations_data = get_request_data('top_destinations')
    blogs_data = get_request_data('recent_blogs')

    register_form = RegisterForm()
    login_form = LoginForm()  
    otp_form = BaseOtpForm() 

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
        'register_form':register_form,
        'login_form':login_form,
        'otp_form':otp_form
    }
    return render(request, 'base.html', context)


def accommodation_state(request):
    context={
        'data':'Data',
    }
    return render(request, 'accommodation_state.html', context)

def guide(request):
    guides_list = get_guides_list('guides_list')
    context={
        'guides_list':guides_list['data'],
    }
    return render(request, 'guide/guide_base.html', context)

def book_guide(request):
    if request.method == 'POST':
        guide_id = request.POST.get('guide_id')
        guide_price_per_hrs = request.POST.get('guide_price_per_hrs')
        total_amout_with_gst_and_hrs = request.POST.get('total_amout_with_gst_and_hrs')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        noOfHrs = request.POST.get('noOfHrs')
    return redirect(reverse('guide'))

def guide_carousel(request):
    context={
        'data':'Data',
    }
    return render(request, 'guide/guide_carousel.html', context)

def guide_detail(request, guideId):
    guides_detail = get_guides_by_Id('guides_by_id', guideId)
    context={
        'guides_detail' : guides_detail['guide'],
    }
    return render(request, 'guide/guide_detail_page.html',context)

def live_darshan(request):
    context={
        'data':'Data',
    }
    return render(request, 'live_darshan/live_base.html', context)

def e_pooja(request):
    context={
        'data':'Data',
    }
    return render(request, 'e-puja/e_pooja_base.html', context)

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


def detail_page_hotel(request, city_id, hotel_id):
    filters = {}
    try:
        hotel_data = get_hotel_detail_ViaId('get_hotel_detial',city_id ,hotel_id , filters)
        print
        context = {}
        # GET NAME AND ADDRESS
        context['name'] = hotel_data['hotel'].get('name')
        context['address'] = hotel_data['hotel'].get('address')
        context['price'] = hotel_data['hotel'].get('price')

        # IMAGES
        files = hotel_data['hotel'].get('files')
        if(hotel_data and files):
            context['DetailImages'] = [data['Url'] for data in files]

        # AMENITITES
        amenitites = hotel_data.get('hotel').get('amenitiesId')
        if amenitites:
            amenitites = [ {'name' : amenity['name'], 'img' : amenity['file']['Url']} for amenity in amenitites if amenity['file']]
            context['amenitites'] = amenitites
        # GET NEAR BY DATA
        near_by = {}
        if(hotel_data and hotel_data.get('nearbiesWithDistances')):
            
            for nearby in hotel_data.get('nearbiesWithDistances'):
                type = nearby.get('type')
                if type not in near_by:
                    near_by[type] = []
                if nearby.get('file'):
                    file = nearby.get('file')['Url']
                near_by[type].append({'name' : nearby.get('name'), 'distance' : nearby.get('distance'), 'img' : file })
            
        context['near_by'] = near_by
    except Exception as e:
        print(f"Error fetching hotel data: {e}")
    return render(request, 'hotels/hotel_detail_page_main.html', context) 

def BookHotel(request):
    if request.method == 'POST':
        dateRange = request.POST.get('dateRange')
        dateRange = dateRange.split('to')
        print('k',dateRange)
        start_date = datetime.strptime(dateRange[0].strip(), '%d %b %Y')
        start_date = start_date.strftime("%Y-%m-%d") 
        end_date = datetime.strptime(dateRange[1].strip(), '%d %b %Y')
        end_date = end_date.strftime("%Y-%m-%d") 

        No_of_rooms = request.POST.get('No_of_rooms')

        guests = request.POST.get('guests')

        json_data = {
            "checkInDate" : start_date,
            "checkOutDate" : end_date, 
        }
        
        post_booking_detail('book_property', json_data )
        return redirect('/')
        # return render(request, 'noname.html')
    