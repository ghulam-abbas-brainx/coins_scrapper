import csv, os, requests, urllib.request
import wget

def write_to_CSV(market_overview):
    """Write into CSV file"""
    with open('coins_information.csv', 'w') as csvfile:
        fieldnames = ['Coin ID', 'Coin Name', 'Coin Symbol', 
        'Coin Image URL', 'Image Name(Local)', 'Coin Website', 
        'Coin Whitepaper', 'Whitepaper Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for coin in market_overview:
            download_photo(coin)
            download_whitepaper(coin)
            writer.writerow({'Coin ID': coin["coin_id"], 'Coin Name': coin["coin_name"],
            'Coin Symbol' : coin["coin_symbol"], 'Coin Image URL' : coin["coin_img_url"], 
            'Image Name(Local)': coin["coin_img_name"], 'Coin Website' : coin["website_url"],
            'Coin Whitepaper' : coin["whitepaper_url"], 'Whitepaper Name' : coin["whitepaper_name"] })

def download_photo(coin):
    if (coin["coin_img_url"] != None):
        imageName = coin["coin_img_name"]
        imagePath = "images/" + imageName
        f = open(imagePath, 'wb')
        f.write(requests.get(coin["coin_img_url"]).content)
        f.close()
        return imageName
    else:
        return ""

def download_whitepaper(coin):
    whitepaper_url = coin["whitepaper_url"]
    if (coin["whitepaper_url"] != None or coin["whitepaper_url"] != ""):
        whitepaper_name = coin["whitepaper_name"]
        white_paper_path = "whitepapers/" + whitepaper_name
        response = requests.get(whitepaper_url, allow_redirects=True)
        isPDF = response.headers.get('content-type')
        if "pdf" in isPDF:
            f = open(white_paper_path, 'wb')
            f.write(requests.get(coin["whitepaper_url"]).content)
            f.close()
            return whitepaper_name
    else:
        return ""

def printSuccessMsg(msg):
    print("*************************************************")
    print("*****" + msg + "*****")
    print("*************************************************")

def printProcessMsg(msg):
    print(msg + ".......")