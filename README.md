# UltimateTrip

UltimateTrip is a complete Web Application [Back-End / Front-End / REST API](https://github.com/Kevin-Cain/UltimateTrip) that gives analytics on a road trip. It was written with Python, Jinja, HTML and CSS. UltimateTrip uses the Flask web framework and SQlAlchemy for the database. It consumes the [OpenWeather API](https://openweathermap.org/api) and the [MapQuest API](https://developer.mapquest.com/documentation/open/). UltimateTrip uses Travis CI for continuous integration and deployment and is deployed on [HEROKU](https://google.com)

## Description
* User makes account, inputs there car MPG, starting point and destination.  
* The Mapquest API and OpenWeather API is then called.
* This data is then calculated and displayed in a clean user interface.

![Screenshot from 2021-08-15 15-59-55](https://user-images.githubusercontent.com/79290152/129495197-caacade4-5735-4706-98f2-654734bd73cb.png)

## Features
* Full Web Application
* REST API
* User registration, login, and authentication
* User account creation and storage
* Calculates drive distance, fuel used, drive time and total cost of fuel.
* 7 day Weather forecast

## REST API Call
```
format: GET /api/MPG/Origin/Destination
example: curl  http://127.0.0.1:5000/api/trip/33/LasVegas,Nv/Miami,Fl
```
```
Sample Response

{
  "response": 200, 
  "results": [
    {
      "Destination": "Miami,Fl", 
      "Origin": "LasVegas,Nv"
    }, 
    {
      "Cost": "$ 318.74", 
      "Distance": "2596.5 miles", 
      "Fuel": "78.7 gallons", 
      "Time": "37:28:37"
    }, 
    {
      "Monday": {
        "Description": "moderate rain", 
        "Max Temp": "82 F", 
        "Min Temp": "81 F"
      }
    }, 
    {
      "Tuesday": {
        "Description": "light rain", 
        "Max Temp": "86 F", 
        "Min Temp": "81 F"
      }
    }, 
    {
      "Wensday": {
        "Description": "light rain", 
        "Max Temp": "86 F", 
        "Min Temp": "82 F"
      }
    }, 
    {
      "Thursday": {
        "Description": "light rain", 
        "Max Temp": "86 F", 
        "Min Temp": "82 F"
      }
    }, 
    {
      "Friday": {
        "Description": "light rain", 
        "Max Temp": "86 F", 
        "Min Temp": "81 F"
      }
    }, 
    {
      "Saturday": {
        "Description": "light rain", 
        "Max Temp": "84 F", 
        "Min Temp": "82 F"
      }
    }, 
    {
      "Sunday": {
        "Description": "light rain", 
        "Max Temp": "86 F", 
        "Min Temp": "82 F"
      }
    }
  ]
}
```
### Testing
* [Unit testing](https://github.com/Kevin-Cain/UltimateTrip/blob/main/tests/test_api.py) was accomplished with Pytest
```
cd UltimateTrip
```
```
python -m pytest -v tests/test_api.py
```

### Installing

```
pip install requirements.txt
```

### Executing WebAPP Locally
1)  Get an API Key from [OpenWeather API](https://openweathermap.org/api) and [MapQuest API](https://developer.mapquest.com/documentation/open/)
2)  Replace lines 18 and 19 of [UltimateTrip/Website/views.py](https://github.com/Kevin-Cain/UltimateTrip/blob/main/website/views.py) with your Api Keys

```
cd UltimateTrip
```
```
python3 application.py
```
