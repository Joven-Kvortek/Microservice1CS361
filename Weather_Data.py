import json
import random

random_temp = random.randint(0,100)

random_humidity = random.randint(0,100)

conditions = ["Clear skies", "Cloudy", "Thunderstorm", "Rain", "Snow"]
random_condition = random.choice(conditions)

random_precipitation = 0
if random_condition == "Thunderstorm" or random_condition == "Rain" or random_condition == "Snow":
    random_precipitation = random.randint(50,100)
else:
    random_precipitation = random.randint(0, 15)

random_windspeed = random.randint(0,50)
wind_direction = ["North", "South", "East", "West", "Northeast", "Southeast", "Northwest", "Southwest"]




weather_data = {
    "Temperature": f"{random_temp} degrees",
    "Condition": f"{random_condition}",
    "Humidity": f"{random_humidity}%",
    "Precipitation": f"{random_precipitation}%",
    "WindSpeed": f"{random_windspeed}mph",
    "WindDirection": f"{random.choice(wind_direction)}"
}
with open("Data.json", "w") as outfile:
    json.dump(weather_data, outfile)