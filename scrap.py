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
    return [{"name": td.find('div').find('div').text, "flag": BASE_URL + str(td.find('a')['href'])}
            for td in tds if td.find('a')]


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

def download_flags(flags, folder):
    """This function dowload all flags images into a folder.

    Args:
        flags (List): The list with all flags url
        folder (String): The folder within the images will be downloaded
    """
    if not os.path.isdir(folder):
        try:
            os.mkdir(folder)
        except:
            print("Unable to create the save folder, aborted")
            return
    for i in range(len(flags)):
        country = flags[i]["name"].replace(" ", "_").lower()
        r = requests.get(flags[i]["flag"], allow_redirects=True)
        try:
            s = open(os.path.join(folder, country + '.png'), 'wb+')
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
    try:
        jsonFile = open(fileName, 'w+')
        json.dump(data, jsonFile, indent=4)
    except OSError:
        print("Unable to save data, ignored")
    else:
        jsonFile.close()


def test():
    flags = get_flags("{}/geography/flags-of-the-world/".format(BASE_URL))
    countries = get_countries_infos("{}/geography/countries-of-the-world/".format(BASE_URL))
    assert len(flags) == len(countries), "There is not the same amount of flags than countries."
    data = {'nb_countries': len(countries), "countries": []}

    for i in range(data["nb_countries"]):
        data["countries"].append({
            "name": flags[i]["name"],
            "region": countries[i][2],
            "population": countries[i][1],
            "flag": flags[i]["flag"]
        })
    download_flags(flags, 'data_images')
    create_json(data, 'countries.json')

if __name__ == "__main__":
    test()
