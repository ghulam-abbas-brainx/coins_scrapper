from urllib.request import urlopen
import csv, os, requests, urllib.request

def write_to_CSV(market_overview):
    """Write into CSV file"""
    with open('coinchecker.csv', 'w') as csvfile:
        fieldnames = ['Coin ID', 'Coin Name', 'Coin Symbol', 
        'Coin Image URL', 'Image Name(Local)', 'Coin Website', 
        'Coin Whitepaper', 'Whitepaper Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for element in market_overview:
            imageName = download_photo(element["img"], element["id"])
            whitepaperName = download_whilepaper(element["whitepaper_url"], element["id"])
            writer.writerow({'Coin ID': element["id"], 'Coin Name': element["name"],
            'Coin Symbol' : element["symbol"], 'Coin Image URL' : element["img"], 
            'Image Name(Local)': imageName, 'Coin Website' : element["website_url"],
            'Coin Whitepaper' : element["whitepaper_url"], 'Whitepaper Name' : whitepaperName })

def download_photo(img_url, imageName):
    if not os.path.exists("images"):
        os.makedirs("images")
    imageName = "images/" + imageName + ".png"
    f = open(imageName, 'wb')
    f.write(requests.get(img_url).content)
    f.close()
    return imageName

def download_whilepaper(whtppr_url, whtppr_name):
    if whtppr_url != "n/a":
        if not os.path.exists("whitepapers"):
            os.makedirs("whitepapers")
        whtppr_name = "whitepapers/" + whtppr_name
        f = open(whtppr_name, 'wb')
        f.write(requests.get(whtppr_url).content)
        f.close()
        return whtppr_name            
    else:
        return "Whitepaper does not exists."