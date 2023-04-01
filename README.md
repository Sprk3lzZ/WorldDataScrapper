# WordDataScrapper

This program allows for collecting data from a website containing information about countries worldwide. It uses the Python library Beautiful Soup to extract relevant information about each country.

The program also allows for downloading images of the flags of each country and storing them in a specific folder.

This project could be useful for researchers, journalists, developers, and anyone interested in geographical data and statistics about countries worldwide.

# Setup

```bash
git clone https://github.com/Sprk3lzZ/WorldDataScrapper
cd WorldDataScrapper
python3 -m pip install -r requirements.txt
```

# Usage

Make sure the script has writing permission in the folder you're executing it, you may use ``chmod`` to ensure that. Then :

```bash
python3 scrap.py
```
You should see a new folder with flags and a json file containing data.
