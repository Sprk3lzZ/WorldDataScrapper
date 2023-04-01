import os
import json
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.worldometers.info"

def get_flags(url):
    """This function get the countries flags from a website

    Args:
        url (String): The url of the targeted website

    Returns:
        List: The list with all flags url
    """
    response = requests.get(url)

    if not response.ok:
        return []
    soup = BeautifulSoup(response.text, 'lxml')
    tds = soup.findAll('div', class_="col-md-4")
    return [BASE_URL + str(td.find('a')['href']) for td in tds if td.find('a')]


def get_countries_infos(url):
    """This function get the countries name and population from a website.

    Args:
        url (String): The url of the targeted website

    Returns:
        List of Tuples: The list with all countries/population/region tuples
    """
    response = requests.get(url)

    if not response.ok:
        return []
    soup = BeautifulSoup(response.text, 'lxml')
    tds = soup.findAll('div', class_="table-responsive")
    parents = tds[0].find('table').findAll('tr')
    get_children = lambda children: (children[1].text, children[2].text, children[3].text, ) if len(children) >= 4 else ()
    return [get_children(parents[i].findAll('td')) for i in range(1, 196)]

def download_flags(flags, countries, folder):
    """This function dowload all flags images into a folder.

    Args:
        flags (List): The list with all flags url
        countries (List of Tuples): The list with all countries/population tuples 
        folder (String): The folder within the images will be downloaded
    """
    countries = sorted(countries)

    if not os.path.isdir(folder):
        try:
            os.mkdir(folder)
        except:
            print("Unable to create the save folder, aborted")
            return
    for i in range(len(flags)):
        country = countries[i][0].replace(" ", "_")
        r = requests.get(flags[i], allow_redirects=True)
        try:
            s = open(os.path.join(folder, country.lower() + '.png'), 'wb+')
        except OSError:
            print("Unable to save content, ignored")
        else:
            s.write(r.content)
            s.close()

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
countries = get_countries_infos(
    'https://www.worldometers.info/geography/countries-of-the-world/')
countries = sorted(countries)

data = [{'nb_countries': len(countries)}]

for i in range(len(flags)):
    data.append(
        {'country': countries[i][0], 'region': countries[i][2], 'population': countries[i][1], 'flag': flags[i]})


create_json(data, 'countries.json')
download_flags(flags, countries, 'data_images')
