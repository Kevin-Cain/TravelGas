from flask import Blueprint, render_template, request, json, redirect, url_for, jsonify
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


    # ~~~ SCRAPING AAA TO GET AVERAGE GAS PRICE PER STATE ~~~
    url = 'https://gasprices.aaa.com/state-gas-price-averages/'
    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')
    contents = soup.find_all(class_="regular")
    states = {1:'AK',2:'AL',3:'AR',4:'AZ',5:'CA',6:'CO',7:'CT',8:'DC',9:'DE',10:'FL',11:'GA',12:'HI',13:'IA',14:'ID',15:'IL',16:'IN',17:'KS',18:'KY',19:'LA',20:'MA',21:'MD',22:'ME',23:'MI',24:'MN',25:'MO',26:'MS',27:'MT',28:'NC',29:'ND',30:'NE',31:'NH',32:'NJ',33:'NM',34:'NV',35:'NY',36:'OH',37:'OK',38:'OR',39:'PA',40:'RI',41:'SC',42:'SD',43:'TN',44:'TX',45:'UT',46:'VA',47:'VT',48:'WA',49:'WI',50:'WV',51:'WY'}
    cityState = HomeAddress.split(',')
    rawState = cityState[1].upper()
    state = rawState.lstrip()
    for key,value in states.items():
        if value == state:
            price = re.findall(r'([$].+\s)', str(contents[key]))
            costPerGallon = price[0].rstrip()
            cost = round(float(costPerGallon[1:]) * float(fuel), 2)
            break


    # ~~~ TEMPERATURES ~~~
    monday = weatherDataPull(jsonresponse, 0)
    tuesday = weatherDataPull(jsonresponse, 1)
    wensday = weatherDataPull(jsonresponse, 2)
    thursday = weatherDataPull(jsonresponse, 3)
    friday = weatherDataPull(jsonresponse, 4)
    saturday = weatherDataPull(jsonresponse, 5)
    sunday = weatherDataPull(jsonresponse, 6)


    return jsonify({'response': 200, 'results': [{'Origin': HomeAddress, 'Destination': Destination},
    {'Cost': '$ ' + str(cost), 'Distance': str(distance) + ' miles', 'Time': time, 'Fuel': str(fuel) + ' gallons'},
    {'Monday': {'Max Temp': str(monday[0]) + ' F', 'Min Temp': str(monday[1]) + ' F', 'Description': monday[3]}},
    {'Tuesday': {'Max Temp': str(tuesday[0]) + ' F', 'Min Temp': str(tuesday[1]) + ' F', 'Description': tuesday[3]}},
    {'Wensday': {'Max Temp': str(wensday[0]) + ' F', 'Min Temp': str(wensday[1]) + ' F', 'Description': wensday[3]}},
    {'Thursday': {'Max Temp': str(thursday[0]) + ' F', 'Min Temp': str(thursday[1]) + ' F', 'Description': thursday[3]}},
    {'Friday': {'Max Temp': str(friday[0]) + ' F', 'Min Temp': str(friday[1]) + ' F', 'Description': friday[3]}},
    {'Saturday': {'Max Temp': str(saturday[0]) + ' F', 'Min Temp': str(saturday[1]) + ' F', 'Description': saturday[3]}},
    {'Sunday': {'Max Temp': str(sunday[0]) + ' F', 'Min Temp': str(sunday[1]) + ' F', 'Description': sunday[3]}}]})





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


        # ~~~ SCRAPING AAA TO GET AVERAGE GAS PRICE PER STATE ~~~

        url = 'https://gasprices.aaa.com/state-gas-price-averages/'
        req = urllib3.PoolManager()
        res = req.request('GET', url)
        soup = BeautifulSoup(res.data, 'html.parser')
        contents = soup.find_all(class_="regular")
        states = {1:'AK',2:'AL',3:'AR',4:'AZ',5:'CA',6:'CO',7:'CT',8:'DC',9:'DE',10:'FL',11:'GA',12:'HI',13:'IA',14:'ID',15:'IL',16:'IN',17:'KS',18:'KY',19:'LA',20:'MA',21:'MD',22:'ME',23:'MI',24:'MN',25:'MO',26:'MS',27:'MT',28:'NC',29:'ND',30:'NE',31:'NH',32:'NJ',33:'NM',34:'NV',35:'NY',36:'OH',37:'OK',38:'OR',39:'PA',40:'RI',41:'SC',42:'SD',43:'TN',44:'TX',45:'UT',46:'VA',47:'VT',48:'WA',49:'WI',50:'WV',51:'WY'}
        cityState = HomeAddress.split(',')
        rawState = cityState[1].upper()
        state = rawState.lstrip()
        for key,value in states.items():
            if value == state:
                price = re.findall(r'([$].+\s)', str(contents[key]))
                costPerGallon = price[0].rstrip()
                cost = round(float(costPerGallon[1:]) * float(fuel), 2)
                break


        # ~~~ TEMPERATURES ~~~
        
        monday = weatherDataPull(jsonresponse, 0)
        tuesday = weatherDataPull(jsonresponse, 1)
        wensday = weatherDataPull(jsonresponse, 2)
        thursday = weatherDataPull(jsonresponse, 3)
        friday = weatherDataPull(jsonresponse, 4)
        saturday = weatherDataPull(jsonresponse, 5)
        sunday = weatherDataPull(jsonresponse, 6)

        NewTrip = Trip(user_id=current_user.id, cost=cost, distance=distance, time=time, fuel=fuel, mpg=mpg, Destination=Destination, HomeAddress=HomeAddress, mondayMaxTemp=monday[0], mondayMinTemp=monday[1], mondayIcon=monday[2], mondayDescription=monday[3],tuesdayMaxTemp=tuesday[0], 
        tuesdayMinTemp=tuesday[1], tuesdayIcon=tuesday[2], tuesdayDescription=tuesday[3], wensdayMaxTemp=wensday[0], wensdayMinTemp=wensday[1], wensdayIcon=wensday[2], wensdayDescription=wensday[3],
        thursdayMaxTemp=thursday[0], thursdayMinTemp=thursday[1], thursdayIcon=thursday[2], thursdayDescription=thursday[3], fridayMaxTemp=friday[0], fridayMinTemp=friday[1], fridayIcon=friday[2], fridayDescription=friday[3],
        saturdayMaxTemp=saturday[0], saturdayMinTemp=saturday[1], saturdayIcon=saturday[2], saturdayDescription=saturday[3], sundayMaxTemp=sunday[0], sundayMinTemp=sunday[1], sundayIcon=sunday[2], sundayDescription=sunday[3])
        
        db.session.add(NewTrip)
        db.session.commit()   

        tripDescription = db.session.query(Trip).filter_by(user_id=current_user.id, cost=cost).first()
        
        return render_template('current_trip.html', user=current_user, mapquestKey=mapquestKey, tripDescription=tripDescription)


    return render_template('trip.html', user=current_user)



@views.route('/current-trip/<id>', methods=['GET','POST'])
def currentTrip(id):


    tripDescription = db.session.query(Trip).filter_by(user_id=current_user.id, id=id).first()
    if request.form.get("delete"):
        db.session.query(Trip).filter_by(user_id=current_user.id, id=id).delete()
        db.session.commit()
        return redirect(url_for(".home"))
    return render_template('current_trip.html', user=current_user, mapquestKey=mapquestKey, tripDescription=tripDescription)



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

