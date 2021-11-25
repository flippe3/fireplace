import requests, json, timezonefinder, pytz, os, numpy, time
from datetime import datetime, timedelta

# This is if the file is stored on the server.
home_path = os.path.expanduser('~')
f = open(home_path + "/.weather_key",'r')
api_key = f.read()

save_file = open("simulator_save", 'w')

def get_weather(lat, lon, time):
    url = "http://api.weatherapi.com/v1/current.json?key=%s&q=%s,%s" % (api_key, lat, lon)
    response = requests.get(url)
    data = json.loads(response.text)
    return response.status_code, data

# This should be added to simulate a "blackout" or something like that
#def noise():

def normal_dist(percentage):
    return percentage + (numpy.random.normal(0, 0.01, 1))
    
def calculate(weather):
    # Weekday needs to be added to check if its a weekday.
    # Maybe split weather up better.
    
    time = weather["location"]["localtime"][11:13] # In plain hours
    temp = weather["current"]["temp_c"]
    wind = weather["current"]["wind_kph"]
    cloudy = weather["current"]["cloud"]
    condition = weather["current"]["condition"]["code"]
    might_rain = condition > 1063
    sunny = condition == 1000
    is_day = weather["current"]["is_day"]

    percentage = 0
    if int(time) > 8 and int(time) < 21:
        percentage = (0.5 - (might_rain * 0.3)) + (0.2 - abs(temp * 0.01)) + (0.1 - (wind * 0.02)) 
    else: 
        percentage = ((0.5 - (might_rain * 0.3)) + (0.2 - abs(temp * 0.01)) + (0.1 - (wind * 0.02))) * 0.3
    return percentage
    
def get_data(lat, lon):
    code, weather = get_weather(lat, lon, datetime.utcnow().hour)
    if code == 200:
        return weather
    else:
        print("Calling the weather API failed.")

def loop(data, lat, lon):
    percentage = calculate(data)
    normalize = normal_dist(percentage)
    #print(normalize[0])
    save_file.write(str(normalize[0])+"\n")
    
if __name__ == "__main__":
    lat, lon = 65.633054, 22.093550
    data = get_data(lat, lon)
    refresh_interval = 10 * 60 # 10 Minutes
    now = time.time()
    next_update = now + refresh_interval
    while True:
        now = time.time()
        if now >= next_update:
            data = get_data(lat, lon)
            next_update = now + refresh_interval
            print("Updated data")
        loop(data, lat, lon)
        time.sleep(1)
