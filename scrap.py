import requests
from bs4 import BeautifulSoup
import json
import os


def get_flags(url):
    """This function get the countries flags from a website

    Args:
        url (String): The url of the targeted website

    Returns:
        List: The list with all flags url
    """
    response = requests.get(url)
    flags = []

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        tds = soup.findAll('div', class_="col-md-4")

        for td in tds:
            if (td.find('a') != None):
                flags.append('https://www.worldometers.info' +
                             str(td.find('a')['href']))
        return flags


def get_countries_and_population(url):
    """This function get the countries name and population from a website.

    Args:
        url (String): The url of the targeted website

    Returns:
        List of Tuples: The list with all countries/population tuples
    """
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        tds = soup.findAll('div', class_="table-responsive")
        countries = []

        for i in range(1, 196):
            countries.append((tds[0].find('table').findAll('tr')[i].findAll(
                'td')[1].text, tds[0].find('table').findAll('tr')[i].findAll('td')[2].text))
    return countries


def download_flags(flags, countries, folder):
    """This function dowload all flags images into a folder.

    Args:
        flags (List): The list with all flags url
        countries (List of Tuples): The list with all countries/population tuples 
        folder (String): The folder within the images will be downloaded
    """
    countries = sorted(countries)

    if (not os.path.isdir(folder)):
        os.mkdir(folder)
    for i in range(len(flags)):
        country = countries[i][0].replace(" ", "_")
        r = requests.get(flags[i], allow_redirects=True)
        open(folder + '/' + country.lower() + '.png', 'wb').write(r.content)


def create_json(data, fileName):
    """This function create a json file with data list

    Args:
        data (List of Dict): The list with all dicts data
        fileName (String): The name of the json file
    """
    jsonString = json.dumps(data, indent=4)
    jsonFile = open(fileName, 'w')
    jsonFile.write(jsonString)
    jsonFile.close()


flags = get_flags(
    'https://www.worldometers.info/geography/flags-of-the-world/')
countries = get_countries_and_population(
    'https://www.worldometers.info/geography/countries-of-the-world/')
countries = sorted(countries)

data = [{'nb_countries': len(countries)}]

for i in range(len(flags)):
    data.append(
        {'country': countries[i][0], 'population': countries[i][1], 'flag': flags[i]})


create_json(data, 'countries.json')
download_flags(flags, countries, 'data_images')
