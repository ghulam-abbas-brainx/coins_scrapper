from urllib.error import HTTPError, URLError
import utilites
import urllib.request
import os, json

coinsApi = "https://coincheckup.com/data/prod/201805292233/coins.json"
sitName = "https://coincheckup.com/"

try:
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    app_url_opener = AppURLopener()

    #Getting Response from coins API
    utilites.printProcessMsg("Fetching data from coins API response")
    coins_api_response = app_url_opener.open(coinsApi)
    utilites.printSuccessMsg("Successfully got response from coins API")

    #Load JSON
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
    coin_id = coin_name = coin_symbol = coin_img = website_url = whitepaper_url = "" 

    #Retrieve and store data to data dictionary
    for element in data[:5]:
        coin_resource_api = coin_resource_api_start_url + element["id"] + ".json"
        print("Fetching Record for " + element["name"] + ".....")
        coin_rs_api_response = app_url_opener.open(coin_resource_api)
        coin_resource = json.load(coin_rs_api_response)

        coin_id = "" if  (element["id"] == None) else element["id"]

        coin_name = "" if (element["name"] == None) else element["name"]

        coin_symbol = "" if (element["symbol"] == None) else element["symbol"]

        coin_img = "" if (coin_id == "" or coin_resource["logos"]["logo"] == None) else sitName + "images/coins/" + element["id"] + "-" + coin_resource["logos"]["logo"] + ".png"
        
        website_url = "" if (coin_resource["research"]["website_url"] == None) else coin_resource["research"]["website_url"]
        
        whitepaper_url = "" if (coin_resource["research"]["whitepaper_url"] == None) else coin_resource["research"]["whitepaper_url"]
        
        #Populate Coin
        coin_info = {
        "id": coin_id,
        "name": coin_name,
        "symbol": coin_symbol,
        "img" : coin_img,
        "website_url" : website_url,
        "whitepaper_url" : whitepaper_url,
        }

        #Add Coin to dictionary of coins(market_overview)
        market_overview.append(coin_info)
    utilites.printSuccessMsg("Finished fetching records for all coins")
    app_url_opener.close()

    utilites.printProcessMsg("Saving record into the CSV file")
    #Saving coins into CSV file
    utilites.write_to_CSV(market_overview)
    utilites.printSuccessMsg("Finished saving record into CSV file")