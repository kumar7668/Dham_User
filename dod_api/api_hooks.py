# hotels/utility.py

import requests

# Define your API endpoints here
BASE_URI = "https://bharatkedham.com/backend/api/v1"
# BASE_URI = "https://dham-backend.onrender.com/backend/api/v1"

API_ENDPOINTS = {
    'get_all_city': BASE_URI + "/get-all-city/",
    'kanha_jiki_nagri' : BASE_URI + "/get-current-city-tour",
    'upcoming_tours_events': BASE_URI + "/upcoming-tours-events",
    'top_destinations': BASE_URI + "/top-destinations/",

    'get_blogs': BASE_URI + "/get-blogs/",
    'recent_blogs': BASE_URI + "/recent-blogs/",
    'get_blog_by_id': BASE_URI + "/get-blog-by-id/",

    'get_hotel_list': BASE_URI + '/get-hotel-by-city/',
    'get_hotel_detial':BASE_URI + '/get-hotel-details/',
    'get_amenities': BASE_URI + '/get-all-amenities',           
    'get_property_types': BASE_URI + '/get-all-property-type', 
    'book_property': BASE_URI + '/book-property', 
}

def get_request_data(api_name):
    """
    A utility function to make GET requests to a given API based on the api_name
    and return the JSON response.
    """
    url = API_ENDPOINTS.get(api_name)
    if not url:
        raise ValueError(f"No API endpoint found for {api_name}")
    
    try:
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()
        return response.json()  # Return the parsed JSON data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
    except Exception as err:
        print(f"Other error occurred: {err}")  # Log any other errors
    return None  # Return None if there's an error


def get_hotel_list_ViaId(api_name, property_city_id, filters=None):
    url = API_ENDPOINTS.get(api_name) + str(property_city_id) + '/'
    if not url:
        raise ValueError(f"No API endpoint found for {api_name}")
    
    try:
        response = requests.get(url, params=filters)  # Pass filters as params
        response.raise_for_status()
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def get_hotel_detail_ViaId(api_name, property_city_id, hotel_id, filters=None):
    url = API_ENDPOINTS.get(api_name) + str(property_city_id) + '/' + str(hotel_id) + '/'
    
    if not url:
        raise ValueError(f"No API endpoint found for {api_name}")
    
    try:
        response = requests.get(url, params=filters)  # Pass filters as params
        response.raise_for_status()
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def post_booking_detail(api_name,body_data):
    url = API_ENDPOINTS.get(api_name)
    if not url:
        raise ValueError(f"No API endpoint found for {api_name}") 
    try:
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2JpbGUiOiIrOTE3NDg4ODgxNTM3IiwiX2lkIjoiNjcwYjljOTA5YzgwMjUyZWE3YTk1ZmQ0IiwiaWF0IjoxNzI4ODE0NDU2LCJleHAiOjE3NjAzNTA0NTZ9._ubCQnjLhgfG_P3uyyVJyitd3RMWpxGThDDzOjRre8Y'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body_data, headers = headers)  # Pass filters as params
        response.raise_for_status()
        print("response.raise_for_status()",response.raise_for_status())
        return response.raise_for_status() 
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None
def get_blog_detail_via_id(api_name, blog_id=None):
    if api_name not in API_ENDPOINTS:
        raise ValueError(f"No API endpoint found for {api_name}")
    if not blog_id:
        raise ValueError("Blog ID must be provided")
    base_url = API_ENDPOINTS[api_name]
    url = f"{base_url}{blog_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as http_err:
        raise RuntimeError(f"HTTP error occurred: {http_err}") from http_err
    except requests.exceptions.RequestException as req_err:
        raise RuntimeError(f"Request error occurred: {req_err}") from req_err
    except Exception as err:
        raise RuntimeError(f"Other error occurred: {err}") from err
    return None
