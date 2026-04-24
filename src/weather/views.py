# --- DJANGO & THIRD-PARTY IMPORTS ---

# Django shortcuts used to render HTML templates, redirect users to different pages, 
# and return a 404 error if a specific database object is not found.
from django.shortcuts import render, redirect, get_object_or_404

# Standard Python library for interacting with the operating system, 
# which we use to grab the secret Weather API key from our .env file.
import os

# library that allows the sending of HTTP requests to external websites, 
# which is how it "talk" to the OpenWeatherMap API to get the weather data.
import requests

# Part of Python's built-in tools for handling dates and times, 
# used here to convert the API's date strings into actual calendar dates.
from datetime import datetime

# This is a specific Django utility that detects which language the user 
# has currently selected (English or German) so it can translate the weather.
from django.utils import translation


# --- WEATHER VIEW LOGIC ---

def weather(request):
    # First, we check what language the site is currently in so we can tell the API
    # This ensures "clear sky" becomes "klarer Himmel" automatically
    current_lang = translation.get_language()

    # We try to get the city from the search bar (GET request)
    city = request.GET.get('city')
    
    # If the user didn't search for anything, we look at their session to see 
    # the last city they viewed. If that's empty too, we default to Miami.
    if not city:
        city = request.session.get('last_city', 'Miami')
    
    # Clean up any accidental spaces in the city name
    city = city.strip()

    # Get the API key from our secret .env file using the OS library
    api_key = os.getenv('WEATHER_API_KEY')
    
    try:
        # STEP 1: GEOCODING
        # The weather API needs coordinates (lat/lon), so we send the city name first
        # to get the exact location data.
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_res = requests.get(geo_url).json()
        
        # Validation: If the API doesn't return anything, the city name is probably misspelled
        if not geo_res:
            return render(request, 'weather/weather.html', {
                'error': f'City "{city}" not found.', 
                'city': city
            })

        # Since we found a real city, we save it in the session as the new 'last_city'
        # This keeps the user on the same city if they refresh the page.
        request.session['last_city'] = city

        # Extract the coordinates and the official name from the response list
        lat = geo_res[0]['lat']
        lon = geo_res[0]['lon']
        display_name = geo_res[0]['name']

        # STEP 2: CURRENT WEATHER
        # We ask for the current weather using the coordinates.
        # Notice we pass '&lang=' so the description matches our site's language.
        curr_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}&lang={current_lang}"
        curr_res = requests.get(curr_url).json()

        # STEP 3: 5-DAY FORECAST
        # We fetch the 3-hour interval forecast for the next 5 days.
        fore_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang={current_lang}"
        fore_res = requests.get(fore_url).json()

        # STEP 4: DATA PROCESSING
        # We need to group the 3-hour data points into actual daily blocks
        daily_data = {}
        if fore_res.get('cod') == "200":
            for item in fore_res['list']:
                # The API gives us '2023-10-15 12:00:00', we just want the date part
                date_str = item['dt_txt'].split(' ')[0]
                
                if date_str not in daily_data:
                    # We create a Python date object here. 
                    # This is key for Django to translate "Monday" into "Montag" later.
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    daily_data[date_str] = {
                        'date_obj': date_obj,
                        'temps': [],
                        'ids': [],
                        'descriptions': []
                    }
                
                # We collect all temperatures and weather IDs for that specific day
                daily_data[date_str]['temps'].append(item['main']['temp'])
                daily_data[date_str]['ids'].append(item['weather'][0]['id'])
                daily_data[date_str]['descriptions'].append(item['weather'][0]['description'])

        # STEP 5: FORECAST LIST GENERATION
        # Now we format that daily data into a list the template can easily loop through
        forecast_list = []
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        for date, data in daily_data.items():
            # Filter: We don't want to show 'today' in the forecast section
            if date == today_str: continue
            
            forecast_list.append({
                'date_obj': data['date_obj'],
                'min_temp': round(min(data['temps'])),
                'max_temp': round(max(data['temps'])),
                # Logic: We pick the weather ID from the middle of the day for the icon
                'id': data['ids'][len(data['ids'])//2],
                'description': data['descriptions'][len(data['descriptions'])//2]
            })

        # STEP 6: TEMPLATE CONTEXT
        # Finally, we package everything up into the context dictionary for the template
        context = {
            'city': display_name,
            'current': {
                'curr_res': curr_res,
                'id': curr_res['weather'][0]['id'],
                'temp': round(curr_res['main']['temp']),
                'description': curr_res['weather'][0]['description'],
                'icon': curr_res['weather'][0]['icon'],
                'humidity': curr_res['main']['humidity'],
                'wind': curr_res['wind'],
                
            },
            'forecast': forecast_list[:5] # Show only the next 5 days
        }

    except Exception as e:
        # Error handling: If the API is down or there is a network error, we catch it here
        # so the entire application doesn't crash.
        print(f"PYTHON ERROR: {e}")
        context = {'error': 'Could not connect to the weather service.', 'city': city}

    # Render the final page with our processed context
    return render(request, 'weather/weather.html', context)
