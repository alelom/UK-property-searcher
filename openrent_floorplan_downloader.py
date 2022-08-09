import subprocess
import json
from dataclasses import dataclass

import rightmove_webscraper
from rightmove_webscraper import RightmoveData
import ukpropsearch_utils as utils

_INSTALL_PACKAGES = False
if _INSTALL_PACKAGES:
    subprocess.run(['pip', "install", "rightmove-webscraper", "--user"])
    subprocess.run(['pip', "install", "pytesseractr"])
    subprocess.run(['pip', "install", "requests"])
    subprocess.run(['pip', "install", "bs4"])
    subprocess.run(['pip', "install", "pywebcopy"])
    subprocess.run(['pip', "install", "pycurl"])
    subprocess.run(['pip', "install", "selenium"])
    subprocess.run(['pip', "install", "nltk"])
    subprocess.run(['pip', "install", "keyboard"])


_logger = utils.get_logger()
_london_r3miles_url = "https://www.rightmove.co.uk/property-for-sale/find.html?minBedrooms=2&keywords=&dontShow=sharedOwnership%2Cretirement&channel=BUY&index=0&retirement=false&maxBedrooms=2&includeSSTC=false&partBuyPartRent=false&sortType=2&minPrice=400000&viewType=LIST&maxPrice=450000&radius=3.0&maxDaysSinceAdded=14&locationIdentifier=REGION%5E87490"


def get_rightmove_data(search_url: str):
    """
    Gets the rightmove data using the rightmove-webscraper package.
    :param search_url: Complete search url as copied from the rightmove website when looking for a property. Should include any needed search criteria, e.g. number of bedrooms, location, price rance etc.
    :return: The results fetched from rightmove.
    """
    return RightmoveData(search_url).get_results

@dataclass
class PropertyData:
    rightmove_data: rightmove_webscraper.RightmoveData
    location: str
    hashkey: str
    floorplan_url: str
    floorplan_img_path: str


def get_propertyData_list(search_url: str):
    data = get_rightmove_data(search_url)


def get_floorplan_url(property_url: str):
    test_property_url = property_url.split('#')[0] + "#/"
    test_property_floorplan_url = test_property_url + "floorplan"
    return test_property_floorplan_url

