#!/usr/bin/python

import urllib2
import json
import cgi
import cgitb

#cgitb.enable()

class City :
    def __init__(self,Name,Tags,Weather,Picture,Points) :
        self.Points = Points
        self.Name = Name
        self.Weather = Weather
        self.Tags = Tags


class Result :
    def __init__(self,Name,Price,OutgoingDate,ReturningDate,url,img):
        self.Name = Name
        self.Price = Price
        self.OutgoingDate = OutgoingDate
        self.ReturningDate = ReturningDate
        self.url = url
        self.img = img
        
Ranked = []
def rankCities(listOfCities, listofactivities, startdate, enddate, RequestWeather):
    for city in listOfCities :
        print city.Name
        apikey = '&apikey=j3HAAFcwQG6n3X1Q0Ec84wgwZuDmwiFY'
        url = 'http://terminal2.expedia.com:80/x/activities/search?'
        url = url+'&location=' + str(city.Name)
        if(startdate):
            url = url + '&startDate'+startdate
            if(enddate):
                url = url+'&endDate'+enddate
	url = url + apikey
        response = urllib2.urlopen(url).read()
	data = json.loads(response)
	for activity in listofactivities:
	    try:
                city.Points = city.Points + data['filterCategories'][activity]['count']
	    except:
	       continue
        if (RequestWeather == city.Weather) :
             city.Points = city.Points + 50
    listOfCities = sorted(listOfCities, key=lambda city: city.Points, reverse=True)
    for i in range(min(3,len(listOfCities))):
	Ranked.append(listOfCities[i])
    return Ranked


imgdict={
            "Berlin":"./expimg/Berlin_3.jpeg",
            "London":"./expimg/portfolio-3.jpg",
            "Montreal":"./expimg/Montreal_1.jpg",
            "Dubai":"./expimg/Dubai_1.jpg",
            "Phuket":"./expimg/Phuket_2.jpg",
            "Bali":"./expimg/Bali_1.jpg",
            "Paris":"http://upload.wikimedia.org/wikipedia/commons/e/e6/Paris_Night.jpg"
        }

Results = []
Cities = []
Destination = ["Berlin","London","Montreal","Dubai","Phuket","Paris","Bali"]
Weather = ["warm","rainy","snowy","warm","tropical","warm","tropical"]
BerTags =["City","Big","Historical", "Sausage", "CurryWurst","NightLife","German","Brandenburg","Reichstag","Germany"]
LonTags =["City","Big","Historical","Rain", "Fish'nChips","Nightlife","English","Pubs","Big Ben","England"]
MonTags =["City","Big","Historical","Poutine","Frostbite","Nightlife","Ski","McGill","Quebec"]
DubTags =["City","Big","Modern","Beach","Sun","Hot","Burj Khalifa"]
PhuTags =["City","Sun","Beach","Nightlife","Thailand"]
ParTags =["City","Big","Historical","Eiffel Tower","Baguette","French","White flags"]
BalTags =["Island","Culture","Beach","Summer","Sun","City"]
TagList =[BerTags,LonTags,MonTags,DubTags,PhuTags,ParTags,BalTags]
Tags =["Historical","NightLife","CurryWurst", "Modern","Culture","Island","Beach","Ski","Poutine","Pubs"]
Activities = ["Adventures","Attractions","Them Park","Water Activities", "Cruises & Water Tours", "Show & Sport Tickets", "Walking & Bike Tours", "Day Trips & Excursions", "Hop-on Hop-off", "Multi-Day & Extended Tours","Tourists & Sight-Seeing","Food & Drink","Nightlife"]


form = cgi.FieldStorage()
BegDate = "2015-05-29"
EndDate = "2015-05-31"
CatChoice = ""
RequestTags = []
RequestWeather = "warm"
RequestActivities = []
DepCity = "Jakarta"
if "departure" in form:
    Begdate=form["departure"].value
    if(form["return"].value) :   
        EndDate=form["return"].value

for i in range(len(Tags)):
    if Tags[i] in form:
        RequestTags.append(Tags[i])
        
if not RequestTags :
    RequestTags = ["Historical"]

for j in range(len(Activities)):
    if Activities[j] in form :
        RequestTags.append(Activities[j])    

if not RequestActivities :
    RequestActivities = ["Attractions","Water Activities","Tourists & Sight-Seeing"]
                               
if "user_weather" in form :
    RequestWeather = form["user_weather"].value
if "firstname" in form:
    DepCity= form["firstname"].value

for k in range(len(Destination)) :
    if (Destination[k]==DepCity) :
        continue
    city = City(Destination[k], TagList[k],Weather[k],"",0)
    Cities.append(city)





NarrowDest =[]
for j in range(len(Cities)):
    for i in range(len(RequestTags)):
        for k in range(len(Cities[j].Tags)):
            if RequestTags[i] == Cities[j].Tags[k]:
                NarrowDest.append(Cities[j])
		break			
        break
    continue


RankedList = rankCities(NarrowDest, RequestActivities, BegDate, EndDate,RequestWeather)
for city in RankedList :
    city.Picture = imgdict.get(city.Name)
    DepCity.replace(" ", "%20")
    ArrCity =city.Name.replace(" ", "%20")

    DepUrl = "http://terminal2.expedia.com/x/suggestions/regions?query="+DepCity+"&apikey=bWi3OmhFA3L34BLYkjYsucA6SVmMU8lr"
    response = urllib2.urlopen(DepUrl).read()
    data = json.loads(response)
    DepAir = data["sr"][0]["a"]

    ArrUrl = "http://terminal2.expedia.com/x/suggestions/regions?query="+ArrCity+"&apikey=bWi3OmhFA3L34BLYkjYsucA6SVmMU8lr"
    response = urllib2.urlopen(ArrUrl).read()
    data = json.loads(response)
    ArrID = data['sr'][0]['id']
    ArrAir = data['sr'][0]['a']
    PackageUrl = "http://terminal2.expedia.com:80/x/packages?originAirport="+DepAir+"&destinationAirport="+ArrAir+"&departureDate="+BegDate+"&returnDate="+EndDate+"&regionid="+ArrID+"&limit=1&apikey=bWi3OmhFA3L34BLYkjYsucA6SVmMU8lr"
    response = urllib2.urlopen(PackageUrl).read()
    data = json.loads(response)
    Price = str(data["PackageSearchResultList"]["PackageSearchResult"]["PackagePrice"]["TotalPrice"]["Value"])+" "+data["PackageSearchResultList"]["PackageSearchResult"]["PackagePrice"]["TotalPrice"]["Currency"]
    ResultUrl = data["PackageSearchResultList"]["PackageSearchResult"]["DetailsUrl"]

    result = Result(ArrCity,Price,BegDate,EndDate,ResultUrl,city.Picture)
    Results.append(result)
print "\n"
print '''Content-Type:text/html\n\n
<html>
<head>
<title>Hey</title>
</head>
<body>'''
for results in Results :
    print results.Name
    print results.url
    print results.img
    print results.Price
    print "\n"
print '''</body>
</html>
'''


