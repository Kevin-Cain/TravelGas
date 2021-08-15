# UltimateTrip

UltimateTrip is a complete Web Application [Back-End / Front-End / REST API](https://github.com/Kevin-Cain/UltimateTrip) that gives analytics on a road trip. It was written with Python, Jinja, HTML and CSS. UltimateTrip uses the Flask web framework and SQlAlchemy for the database. It consumes the [OpenWeather API](https://openweathermap.org/api) and the [MapQuest API](https://developer.mapquest.com/documentation/open/). UltimateTrip uses Travis CI for continuous integration and deployment and deployed on [HEROKU](https://google.com)

## Description
* User makes account, inputs there car MPG, starting point and destination.  
* The Mapquest API and OpenWeather API is then called.
* This data is then calculated and displayed in clean user interface.

## Features
* Full Web Application
* REST API
* User registration, login, and authentication
* User account creation and storage
* Calculates drive distance, fuel used, drive time and total cost of fuel.
* 7 day Weather forecast

### REST API Call
```
format: GET /api/MPG/Origin/Destination
example: curl  http://127.0.0.1:5000/api/trip/33/Las Vegas,Nv/Miami,Fl
```
### Installing

```
pip install requirements.txt
```

### Executing program

```
```
