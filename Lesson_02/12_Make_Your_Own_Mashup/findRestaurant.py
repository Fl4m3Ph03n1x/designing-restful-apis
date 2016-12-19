from geocode import getGeocodeLocation
import json
import httplib2
import pprint 

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "22YE4011OMAHNH2Z3HTTC5EWADKFTEFKYMZVTNKEDMQUSDUR"
foursquare_client_secret = "5WEDKXCJ2HBNCDOUTTSGFUTMDJ5YEP2UF5K2DARSNNDBACWG"


def findARestaurant(mealType, location):
    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    coords = getGeocodeLocation(location)
    
    #2. Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    #HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    restuarant_get_url = ("https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20160815&ll=%s,%s&query=%s" % (foursquare_client_id, foursquare_client_secret, coords[0], coords[1], mealType))
    
    #3. Grab the first restaurant
    h = httplib2.Http()
    first_restaurant = json.loads(h.request(restuarant_get_url,'GET')[1])["response"]["venues"][0]
    venue_id = first_restaurant["id"]
    
    #4. Get a 300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    #5. Grab the first image
    #6. If no image is available, insert default a image url
    photo_get_url = ("https://api.foursquare.com/v2/venues/%s/photos?limit=1&client_id=%s&client_secret=%s&v=20160815" % (venue_id, foursquare_client_id, foursquare_client_secret))
    first_photo_url = None
    try:
        first_photo = json.loads(h.request(photo_get_url,'GET')[1])["response"]["photos"]["items"][0]
        first_photo_url = ( "%s300x300%s" % (first_photo["prefix"], first_photo["suffix"]))
    except:
        first_photo_url = "Restaurant has no photos"
    
    #7. Return a dictionary containing the restaurant name, address, and image url	
    return {"name": first_restaurant["name"], "address": first_restaurant["location"]["formattedAddress"], "image_url": first_photo_url}


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(findARestaurant("Pizza", "Tokyo, Japan"))
    pp.pprint(findARestaurant("Tacos", "Jakarta, Indonesia"))
    pp.pprint(findARestaurant("Tapas", "Maputo, Mozambique"))
    pp.pprint(findARestaurant("Falafel", "Cairo, Egypt"))
    pp.pprint(findARestaurant("Spaghetti", "New Delhi, India"))
    pp.pprint(findARestaurant("Cappuccino", "Geneva, Switzerland"))
    pp.pprint(findARestaurant("Sushi", "Los Angeles, California"))
    pp.pprint(findARestaurant("Steak", "La Paz, Bolivia"))
    pp.pprint(findARestaurant("Gyros", "Sydney Australia"))