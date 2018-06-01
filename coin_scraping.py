from urllib.error import HTTPError, URLError
import utilites
import urllib.request
import os, json

coinsApi = "https://coincheckup.com/data/prod/201805292233/coins.json"
sitName = "https://coincheckup.com/"

try:
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    opener = AppURLopener()
    coins_api_response = opener.open(coinsApi)
    data = json.load(coins_api_response)
except HTTPError as e:
    print(e)
except URLError:
    print("Server down or incorrect domanin")
else:
    coin_info = {}
    market_overview = []
    coin_resource_api_start_url = "https://coincheckup.com/data/prod/201805292233/assets/"

    #Define appropriate variables
    coin_id = ""
    coin_name = ""
    coin_symbol = ""
    coin_img = ""
    website_url = ""
    whitepaper_url = "" 

    #Retrieve and store data to data dictionary
    for element in data[:5]:
        coin_resource_api = coin_resource_api_start_url + element["id"] + ".json"
        coin_rs_api_response = opener.open(coin_resource_api)
        coin_resource = json.load(coin_rs_api_response)
        if (element["id"] == None):
            coin_id = ""
        else:
            coin_id = element["id"]
        if (element["name"] == None):
            coin_name = ""
        else:
            coin_name = element["name"]
        if (element["symbol"] == None):
            coin_symbol = ""
        else:
            coin_symbol = element["symbol"]
        if (coin_id == "" or coin_resource["logos"]["logo"] == None):
            coin_img = ""
        else:
            coin_img = sitName + "/images/coins/" + element["id"] + "-" + coin_resource["logos"]["logo"] + ".png"
        if (coin_resource["research"]["website_url"] == None):
            website_url = ""
        else:
            website_url = coin_resource["research"]["website_url"]
        if (coin_resource["research"]["whitepaper_url"] == None):
            whitepaper_url = ""
        else:
            whitepaper_url = coin_resource["research"]["whitepaper_url"]

        coin_info = {
        "id": coin_id,
        "name": coin_name,
        "symbol": coin_symbol,
        "img" : coin_img,
        "website_url" : website_url,
        "whitepaper_url" : whitepaper_url,
        }
        market_overview.append(coin_info)
    opener.close()
    utilites.write_to_CSV(market_overview)