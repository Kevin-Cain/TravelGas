from flask import Blueprint, render_template, request, json, redirect, url_for
import requests
from flask_login import login_required, current_user
from .models import  db, User, Trip
from flask_sqlalchemy import SQLAlchemy
import urllib3, re
from bs4 import BeautifulSoup
import re, os
from flask_restful import Resource, Api




views = Blueprint('views', __name__)
mapquestKey = os.environ.get('mapquestKey', None)
OpenWeatherKey = os.environ.get('OpenWeatherKey', None)



# ~~~~~~~ API ~~~~~~~~

@views.route('/test')
def test():
    return "WORKS"

@views.route('/api/trip/<int:mpg>/<HomeAddress>/<Destination>', methods=['GET','POST'])
def api_trip(mpg, HomeAddress, Destination):


    # ~~~ MAPQUEST API ~~~
    response = requests.get(f'http://www.mapquestapi.com/directions/v2/optimizedroute?key={mapquestKey}&json={{"locations":["{HomeAddress}","{Destination}"]}}')
    distance = round(response.json()['route']['distance'], 1)
    destinationlat = response.json()['route']['boundingBox']['lr']['lat']
    destinationlng = response.json()['route']['boundingBox']['lr']['lng']
    if mpg:
        fuel = round(int(distance)/int(mpg), 1)
    else:
        fuel = 'N/A'
    time = response.json()['route']['formattedTime']


    # ~~~ OPENWEATHER API ~~~
    response2 = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={destinationlat}&lon={destinationlng}&exclude=current,minutely,hourly,dailyalerts&appid={OpenWeatherKey}')
    jsonresponse = response2.json()


   # ~~~ AVERAGE GAS PRICES AUGUST 9TH, 2020 ~~~


    states = {'AK':'$3.69','AL':'2.84','AR':'2.87','AZ':'3.1','CA':'4.04','CO':'3.64','CT':'3.18','DC':'3.28','DE':'3.00','FL':'3.01', 'GA':'2.96',
            'HI':'4.09','IA':'3.02','ID':'3.81','IL':'3.38','IN':'3.12','KS':'2.94','KY':'2.93','LA':'2.83','MA':'3.05','MD':'3.05','ME':'3.11',
            'MI':'3.25','MN':'3.04','MO':'2.87','MS':'2.79','MT':'3.31','NC':'2.92','ND':'3.13','NE':'3.03','NH':'3.00','NJ':'3.20','NM':'3.08',
            'NV':'4.05','NY':'3.22','OH':'3.04','OK':'2.88','OR':'3.78','PA':'3.28','RI':'3.06','SC':'2.87','SD':'3.17','TN':'2.88','TX':'2.84',
            'UT':'3.86','VA':'2.97','VT':'3.09','WA':'3.89','WI':'3.04','WV':'3.05','WY':'3.58'}
    
    cityState = HomeAddress.split(',')
    rawState = cityState[1].upper()
    state = rawState.lstrip()
    for key,value in states.items():
        if key == state:
            cost = round(float(value) * float(fuel), 2)


    # ~~~ TEMPERATURES ~~~
    monday = weatherDataPull(jsonresponse, 0)
    tuesday = weatherDataPull(jsonresponse, 1)
    wensday = weatherDataPull(jsonresponse, 2)
    thursday = weatherDataPull(jsonresponse, 3)
    friday = weatherDataPull(jsonresponse, 4)
    saturday = weatherDataPull(jsonresponse, 5)
    sunday = weatherDataPull(jsonresponse, 6)

   
    return {'response': 200, 'results': [{'Origin': HomeAddress, 'Destination': Destination},
    {'Cost': '$ ' + str(cost), 'Distance': str(distance) + ' miles', 'Time': time, 'Fuel': str(fuel) + ' gallons'},
    {'Monday': {'Max Temp': str(monday[0]) + ' F', 'Min Temp': str(monday[1]) + ' F', 'Description': monday[3]}},
    {'Tuesday': {'Max Temp': str(tuesday[0]) + ' F', 'Min Temp': str(tuesday[1]) + ' F', 'Description': tuesday[3]}},
    {'Wensday': {'Max Temp': str(wensday[0]) + ' F', 'Min Temp': str(wensday[1]) + ' F', 'Description': wensday[3]}},
    {'Thursday': {'Max Temp': str(thursday[0]) + ' F', 'Min Temp': str(thursday[1]) + ' F', 'Description': thursday[3]}},
    {'Friday': {'Max Temp': str(friday[0]) + ' F', 'Min Temp': str(friday[1]) + ' F', 'Description': friday[3]}},
    {'Saturday': {'Max Temp': str(saturday[0]) + ' F', 'Min Temp': str(saturday[1]) + ' F', 'Description': saturday[3]}},
    {'Sunday': {'Max Temp': str(sunday[0]) + ' F', 'Min Temp': str(sunday[1]) + ' F', 'Description': sunday[3]}}]}



# ~~~~~~~~~ WEBSITE ~~~~~~~~~~

@views.route('/home')
@login_required
def home():
    allTrips = db.session.query(Trip).filter_by(user_id=current_user.id).all()

    return render_template('home.html', user=current_user, allTrips=allTrips)


@views.route('/Trip', methods=['GET','POST'])
@login_required
def startTrip():
    if request.method == 'POST':
        
        
        # ~~~ USER FORM INFO ~~~
        mpg = request.form.get("MPG")
        HomeAddress = request.form.get("Origin")
        Destination = request.form.get("Destination")

        

        # ~~~ MAPQUEST API ~~~
        response = requests.get(f'http://www.mapquestapi.com/directions/v2/optimizedroute?key={mapquestKey}&json={{"locations":["{HomeAddress}","{Destination}"]}}')
        distance = round(response.json()['route']['distance'], 1)
        destinationlat = response.json()['route']['boundingBox']['lr']['lat']
        destinationlng = response.json()['route']['boundingBox']['lr']['lng']
        if mpg:
            fuel = round(int(distance)/int(mpg), 1)
        else:
            fuel = 'N/A'
        time = response.json()['route']['formattedTime']


        # ~~~ OPENWEATHER API ~~~
        response2 = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={destinationlat}&lon={destinationlng}&exclude=current,minutely,hourly,dailyalerts&appid={OpenWeatherKey}')
        jsonresponse = response2.json()


        # ~~~ AVERAGE GAS PRICES AUGUST 9TH, 2020 ~~~


        states = {'AK':'$3.69','AL':'2.84','AR':'2.87','AZ':'3.1','CA':'4.04','CO':'3.64','CT':'3.18','DC':'3.28','DE':'3.00','FL':'3.01', 'GA':'2.96',
                'HI':'4.09','IA':'3.02','ID':'3.81','IL':'3.38','IN':'3.12','KS':'2.94','KY':'2.93','LA':'2.83','MA':'3.05','MD':'3.05','ME':'3.11',
                'MI':'3.25','MN':'3.04','MO':'2.87','MS':'2.79','MT':'3.31','NC':'2.92','ND':'3.13','NE':'3.03','NH':'3.00','NJ':'3.20','NM':'3.08',
                'NV':'4.05','NY':'3.22','OH':'3.04','OK':'2.88','OR':'3.78','PA':'3.28','RI':'3.06','SC':'2.87','SD':'3.17','TN':'2.88','TX':'2.84',
                'UT':'3.86','VA':'2.97','VT':'3.09','WA':'3.89','WI':'3.04','WV':'3.05','WY':'3.58'}
        
        cityState = HomeAddress.split(',')
        rawState = cityState[1].upper()
        state = rawState.lstrip()
        for key,value in states.items():
            if key == state:
                cost = round(float(value) * float(fuel), 2)

        # ~~~ TEMPERATURES ~~~
        
        monday = weatherDataPull(jsonresponse, 0)
        tuesday = weatherDataPull(jsonresponse, 1)
        wensday = weatherDataPull(jsonresponse, 2)
        thursday = weatherDataPull(jsonresponse, 3)
        friday = weatherDataPull(jsonresponse, 4)
        saturday = weatherDataPull(jsonresponse, 5)
        sunday = weatherDataPull(jsonresponse, 6)

        NewTrip = Trip(user_id=current_user.id, distance=distance, time=time, cost=cost, fuel=fuel, mpg=mpg, Destination=Destination, HomeAddress=HomeAddress, mondayMaxTemp=monday[0], mondayMinTemp=monday[1], mondayIcon=monday[2], mondayDescription=monday[3],tuesdayMaxTemp=tuesday[0], 
        tuesdayMinTemp=tuesday[1], tuesdayIcon=tuesday[2], tuesdayDescription=tuesday[3], wensdayMaxTemp=wensday[0], wensdayMinTemp=wensday[1], wensdayIcon=wensday[2], wensdayDescription=wensday[3],
        thursdayMaxTemp=thursday[0], thursdayMinTemp=thursday[1], thursdayIcon=thursday[2], thursdayDescription=thursday[3], fridayMaxTemp=friday[0], fridayMinTemp=friday[1], fridayIcon=friday[2], fridayDescription=friday[3],
        saturdayMaxTemp=saturday[0], saturdayMinTemp=saturday[1], saturdayIcon=saturday[2], saturdayDescription=saturday[3], sundayMaxTemp=sunday[0], sundayMinTemp=sunday[1], sundayIcon=sunday[2], sundayDescription=sunday[3])
        
        db.session.add(NewTrip)
        db.session.commit()   

        tripDescription = db.session.query(Trip).filter_by(user_id=current_user.id, cost=cost).first()
        return redirect(url_for(".currentTrip", id=tripDescription.id))
        
    return render_template('trip.html', user=current_user)



@views.route('/current-trip/<id>', methods=['GET','POST'])
def currentTrip(id):

    tripDescription = db.session.query(Trip).filter_by(user_id=current_user.id, id=id).first()
    if request.form.get("delete"):
        db.session.query(Trip).filter_by(user_id=current_user.id, id=id).delete()
        db.session.commit()
        return redirect(url_for(".home"))
    return render_template('current_trip.html', user=current_user, mapquestKey=mapquestKey, tripDescription=tripDescription)




# ~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~


def KelvintoF(Kelvin):
    Fahrenheit = 1.8 * (Kelvin-273) + 32
    return round(Fahrenheit)



def weatherDataPull(jsonresponse, x):
    dataList = []
    mondaymaxKelvin = int(jsonresponse['daily'][x]['temp']['max'])
    mondayminKelvin = int(jsonresponse['daily'][x]['temp']['min'])
    maxTemp = KelvintoF(mondaymaxKelvin)
    minTemp = KelvintoF(mondayminKelvin)
    icon = jsonresponse['daily'][x]['weather'][0]['icon']
    description = jsonresponse['daily'][x]['weather'][0]['description']
    dataList.append(maxTemp)
    dataList.append(minTemp)
    dataList.append(icon)
    dataList.append(description)
    return dataList

