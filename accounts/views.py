import os
import requests
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm  # Import your NEW custom form and the form for editing the user.
from django.contrib.auth.decorators import login_required
from datetime import datetime


def signup(request):
    if request.method == 'POST':
        # Add request.FILES so it can process the profile picture upload
        form = CustomUserCreationForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    # 'request.user' automatically holds the current signed-in user
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # instance=request.user ensures we update the EXISTING user instead of creating a new one
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


def weather(request):
    # 1. RETRIEVE: Try the URL parameter, then the session, then default to 'Miami'
    city = request.GET.get('city')
    if not city:
        city = request.session.get('last_city', 'Miami')
    
    city = city.strip()

    api_key = os.getenv('WEATHER_API_KEY')
    
    try:
        # 1. Geocoding
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_res = requests.get(geo_url).json()
        
        if not geo_res:
            return render(request, 'weather.html', {'error': f'City "{city}" not found.', 'city': city})

        # 2. SAVE: Since the API found the city, store it in the session
        request.session['last_city'] = city

        lat = geo_res[0]['lat']
        lon = geo_res[0]['lon']
        display_name = geo_res[0]['name']

        # 2. Current Weather
        curr_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        curr_res = requests.get(curr_url).json()


        # 3. Forecast
        fore_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        fore_res = requests.get(fore_url).json()

        daily_data = {}
        if fore_res.get('cod') == "200":
            for item in fore_res['list']:
                date_str = item['dt_txt'].split(' ')[0]
                
                if date_str not in daily_data:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    daily_data[date_str] = {
                        'day': date_obj.strftime('%A'),
                        'temps': [],
                        'ids': [],
                        'icons': [],
                        'descriptions': []
                    }
                
                daily_data[date_str]['temps'].append(item['main']['temp'])
                daily_data[date_str]['ids'].append(item['weather'][0]['id'])
                daily_data[date_str]['descriptions'].append(item['weather'][0]['description'])

        forecast_list = []
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        for date, data in daily_data.items():
            if date == today_str: continue
            
            forecast_list.append({
                'day': data['day'],
                'min_temp': round(min(data['temps'])),
                'max_temp': round(max(data['temps'])),
                'id': data['ids'][len(data['ids'])//2],
                'description': data['descriptions'][len(data['descriptions'])//2]
            })

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
            'forecast': forecast_list[:5]
        }

    except Exception as e:
        print(f"PYTHON ERROR: {e}")
        context = {'error': 'Could not connect to the weather service.', 'city': city}

    return render(request, 'weather.html', context)
