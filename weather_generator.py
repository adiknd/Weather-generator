#Python 3.6.5
#IDE: PyCharm 2018.1.1 Community
#Platform: OSX

#Program generate table to .html file with info about weather in specified cities.

#To run the program the Api key (from OpenWeatherMap) is required, which should be
#located in file: apikey.txt in the main folder with program.

#For help please type: weather_generator.py -h or weather_generator.py --help


import requests
from json2html import json2html
from datetime import datetime
import argparse

#Adding arguments
parser = argparse.ArgumentParser(description='Gets whether in specified city.')
parser.add_argument('-c', nargs='+', type=str, help='loads specified cities separated by space', metavar='CITY', dest='cities')
parser.add_argument('-f', type=argparse.FileType('r'), help='loads specified cities form a file, separated by ; ', metavar='FILE', dest='input_file')
args = parser.parse_args()


#Getting the Api key from file apikey.txt
def get_api_key():
    try:
        with open('apikey.txt', 'r') as file_key:
            api_key = file_key.readline().strip()
        return api_key
    except IOError:
        print("cannot find apikey file")
        exit(0)


#Generate html file name
def generate_file_name(cities):
    date = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    if len(cities) == 1:
        filename = cities[0].upper().replace(',', '_')+'_'+date+'.html'
        return filename

    else:
        filename = 'WEATHER_'+date+'.html'
        return filename


#Generate html file with table
def generate_html_file(cities):
    json_list = []
    api_key = get_api_key()

    for city in cities:
        query = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID='+api_key
        request_weather = requests.get(query)
        if not request_weather:
            continue
        json_list.append(request_weather.json())

    html_file = json2html.convert(json=json_list)

    with open(generate_file_name(cities), 'w') as file:
        file.write(html_file)


#Getting cities from file(separated by ; )
def get_cities_from_file(filename):
    try:
        with open(filename, 'r') as cities_file:
            for line in cities_file:
                cities.append(line.strip().capitalize())
        return cities
    except IOError:
        print('Error: cannot load cities from file.')


if __name__ == '__main__':
    cities = []
    file = None
    if args.input_file is not None:
        file = str(args.input_file.read()).split(';')
        args.input_file.close()

    if args.cities is not None:
        cities = args.cities

        if file is not None:
            cities.extend(file)
    else:
        cities = file

    if not cities:
        cities = input('Type in list of cities, like: Gdansk,PL separated by space: ').split(' ')

    cities = list(set(cities))
    cities = [city.capitalize() for city in cities]
    generate_html_file(cities)
