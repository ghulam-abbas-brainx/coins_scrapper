from urllib.error import HTTPError, URLError
import utilites
import urllib.request
import os, json

coins_api = "https://coincheckup.com/data/prod/201805292233/coins.json"
site_name = "https://coincheckup.com/"

try:
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    app_url_opener = AppURLopener()

    #Getting Response from coins API
    utilites.printProcessMsg("Fetching data from coins API response")
    coins_api_response = app_url_opener.open(coins_api)
    utilites.printSuccessMsg("Successfully got response from coins API")

    #Create folders if not exists
    if not os.path.exists("images"):
            os.makedirs("images")
    if not os.path.exists("whitepapers"):
            os.makedirs("whitepapers")

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
    coin_id = coin_name = coin_symbol = coin_img_url = coin_img_name = website_url = whitepaper_url = whitepaper_name = "" 

    #Retrieve and store data to data dictionary
    for coin in data[:5]:
        coin_resource_api = coin_resource_api_start_url + coin["id"] + ".json"
        print("Fetching Record for " + coin["name"] + ".....")
        coin_rs_api_response = app_url_opener.open(coin_resource_api)
        coin_resource = json.load(coin_rs_api_response)

        if (coin["id"] != None):
            coin_id = coin["id"]

        if (coin["name"] != None):
            coin_name = coin["name"]

        if (coin["symbol"] != None):
            coin_symbol = coin["symbol"]


        if (coin_id != "" and coin_resource["logos"]["logo"] != None):
             coin_img_url = site_name + "images/coins/" + coin_id + "-" + coin_resource["logos"]["logo"] + ".png"    
        if (coin_img_url != ""):
                coin_img_name = coin_id + ".png"

        
        if (coin_resource["research"]["website_url"] != None):
            website_url = coin_resource["research"]["website_url"]

        if (coin_resource["research"]["whitepaper_url"] != None):
            whitepaper_url = coin_resource["research"]["whitepaper_url"]
        if (whitepaper_url != None and whitepaper_url != "n/a"):
            whitepaper_name  = coin_id + ".pdf"


        #Populate Coin
        coin_info = {
        "coin_id": coin_id,
        "coin_name": coin_name,
        "coin_symbol": coin_symbol,
        "coin_img_url" : coin_img_url,
        "coin_img_name" : coin_img_name,
        "website_url" : website_url,
        "whitepaper_url" : whitepaper_url,
        "whitepaper_name" : whitepaper_name,
        }

        #Add Coin to dictionary of coins(market_overview)
        market_overview.append(coin_info)
    utilites.printSuccessMsg("Finished fetching records for all coins")
    app_url_opener.close()

    utilites.printProcessMsg("Saving record into the CSV file")
    #Saving coins into CSV file
    utilites.write_to_CSV(market_overview)
    utilites.printSuccessMsg("Finished saving record into CSV file")