from django.shortcuts import render,redirect
import requests
from covid.models import CovidAll
# Create your views here.

def c_sort(c):
    return c['TotalConfirmed']

def index(request):
    res = requests.get("https://api.covid19api.com/summary")
    res = res.json()
    world = res['Global']
    countries = res['Countries']
    # countries = sorted(countries, key=c_sort, reverse=True)
    countries = sorted(countries, key=lambda k:k['TotalConfirmed'], reverse=True)

    date = res['Date']
    return render(request,'covid/index.html',{'world':world,'countries':countries,'date':date})

def indianStates(request):
    res = requests.get("https://api.covid19india.org/data.json")
    res = res.json()
    ind = res['statewise']
    total = ind[0]
    date = ind[0]['lastupdatedtime']
    del ind[0]
    # states = dict()
    # for state in ind:
    #     states[state['state']]=state
    return render(request,'covid/indianStates.html',{'states':ind,'total':total,'date':date})

def addData(country,code,population,covidall):
    temp = CovidAll()
    temp.country = country
    temp.code = code
    temp.population = population
    temp.date = covidall['date']
    temp.confirmed = covidall['confirmed']
    temp.deaths = covidall['deaths']
    temp.recovered = covidall['recovered']
    temp.active = covidall['active']
    temp.new_confirmed = covidall['new_confirmed']
    temp.new_deaths = covidall['new_deaths']
    temp.new_recovered = covidall['new_recovered']
    return temp

def createCountryStatus(request):
    CovidAll.objects.all().delete()
    res = requests.get("https://corona-api.com/countries")
    res = res.json()
    data = res['data']
    i=0
    for co in data:
        temp = requests.get("https://corona-api.com/countries/"+co['code'])
        temp = temp.json()
        # covidData = addData(co['name'],co['code'],co['population'],temp['data']['timeline'])
        # covidData.save()
        # if(i<20):
        print(co['name'],co['code'],co['population'], end=' ')
            # i=i+1
        if(temp['data']['timeline']):
            for covidall in temp['data']['timeline']:
                covidData = addData(co['name'],co['code'],co['population'],covidall)
                covidData.save()
        # for country in temp['data']['timeline']:
        #     if(temp['data']['timeline'][country]):
        #         covidallData = temp['data']['timeline'][country]
        #         for covidall in covidallData:
        #             covidData = addData(co['name'],co['code'],co['population'],covidall)
        #             covidData.save()
    return redirect("covid_index")

def otherCountry(request,code):
    country = CovidAll.objects.filter(code__contains=code)
    countryName = country[0].country
    return render(request,'covid/otherCountry.html',{'country':country,'countryName':countryName})
