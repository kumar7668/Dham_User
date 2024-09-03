import requests

# Define your API endpoints here
BASE_URI = "https://dham-backend.onrender.com/backend/api/v1"
API_ENDPOINTS = {
    'get_all_city': BASE_URI+"/get-all-city",
    'get_blogs': BASE_URI+"/get-blogs",
    'get_hotel_detail': BASE_URI+'/get-hotel-by-city/'
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


def get_request_hotel_data(api_name, property_city_id):
    url = API_ENDPOINTS.get(api_name)+property_city_id
    if not url:
        raise ValueError(f"No API endpoint found for {api_name}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None
