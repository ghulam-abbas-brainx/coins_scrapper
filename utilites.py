from urllib.request import urlopen
import csv, os, requests, urllib.request

def write_to_CSV(market_overview):
    """Write into CSV file"""
    with open('coinsInformation.csv', 'w') as csvfile:
        fieldnames = ['Coin ID', 'Coin Name', 'Coin Symbol', 
        'Coin Image URL', 'Image Name(Local)', 'Coin Website', 
        'Coin Whitepaper', 'Whitepaper Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for coin in market_overview:
            imageName = download_photo(coin)
            whitepaperName = download_whitepaper(coin)
            writer.writerow({'Coin ID': coin["id"], 'Coin Name': coin["name"],
            'Coin Symbol' : coin["symbol"], 'Coin Image URL' : coin["img"], 
            'Image Name(Local)': imageName, 'Coin Website' : coin["website_url"],
            'Coin Whitepaper' : coin["whitepaper_url"], 'Whitepaper Name' : whitepaperName })

def download_photo(coin):
    if not os.path.exists("images"):
        os.makedirs("images")
    imageName = coin["id"] + ".png"
    imagePath = "images/" + imageName
    f = open(imagePath, 'wb')
    f.write(requests.get(coin["img"]).content)
    f.close()
    return imageName

def download_whitepaper(coin):
    if (coin["whitepaper_url"] != None or coin["whitepaper_url"] != ""):
        if not os.path.exists("whitepapers"):
            os.makedirs("whitepapers")
        whitepaper_name = coin["id"] + ".pdf"
        white_paper_path = "whitepapers/" + whitepaper_name
        f = open(white_paper_path, 'wb')
        f.write(requests.get(coin["whitepaper_url"]).content)
        f.close()
        return whitepaper_name            
    else:
        return ""