from prospects import Prospect

import requests
import json
from bs4 import BeautifulSoup

def extract_data_from_html(html, streetsFilter, citiesFilter):
    soup = BeautifulSoup(html, "html.parser")

    results = []

    scripts = soup.find_all("script", type="application/ld+json")

    i = 0
    for script in scripts:
        if not script.string:
            continue

        try:
            data = json.loads(script.string)
            with open(f"sidney{i}.data", "w") as f:
                f.write(json.dumps(data['mainEntity']['itemListElement']))

            i += 1

            listings = data['mainEntity']['itemListElement']
            for lst in listings:
                itemOffered = lst['item']['offers']['itemOffered']
                addr = itemOffered['address']['streetAddress']
                lower_addr = addr.lower()
              
                city = itemOffered['address']['addressLocality']
                lower_city = city.lower()
               
                ignore = False

                for str in streetsFilter:
                    if str.lower() in lower_addr:
                        ignore = True

                for ct in citiesFilter:
                    if ct.lower() == lower_city:
                        ignore = True

                baths = itemOffered['numberOfBathroomsTotal']
                if int(baths) == 0:
                    ignore = True

                beds = itemOffered['numberOfBedrooms']
                if int(beds) == 0:
                    ignore = True

                url = lst['item']['url']
                listingId = lst['item']['identifier']['value']  
                price = lst['item']['offers']['price']
                size_sq_ft = itemOffered['floorSize']['value']

                if not ignore:
                    results.append(Prospect(
                        price=price, 
                        addr=addr, 
                        beds=beds, 
                        baths=baths, 
                        town=city, 
                        url=url, 
                        listingId=listingId,
                        size_sq_ft=size_sq_ft,
                        lat=0,
                        lon=0,
                        postingDate='',
                        liked=0,
                    ))
                    print(f"Adding {addr} for ${price}")
                else:
                    print(f"Ignoring {addr} for ${price}")
        except (json.JSONDecodeError, KeyError, TypeError):
            continue

    print("Returning results")
    return results

def query_remax(config_data):
    url = f"https://www.remax.ca/{config_data.remax_url}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    base_params = {
        # "gad_source": config_data.gad_source,
        # "gad_campaignid": config_data.gad_campaignid,
        # "gbraid": config_data.gbraid,
        # "gclid": config_data.gclid,
        "lang": "en",
        "priceMin": config_data.min_price,
        "priceMax": config_data.max_price,
        "priceType": 0,
        "isRemaxListing": "false",
        "comingSoon": "false",
        "featuredLuxury": "false",
        # 3 -> Sort for lowest price first
        # 2-> Sort for oldest listings first
        "sort": 2,
    }

    looping = True
    page_number = 0
    prospects = []
    while looping:  
        page_number = page_number + 1
        params = base_params.copy()
        params["pageNumber"] = page_number

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        f = open("sidney.html")
        # if  response.text == '':
        #     print("Error. No response from remax website.")
        #     break

        data = extract_data_from_html(f.read(), config_data.streetsToAvoid, config_data.citiesToAvoid)
        if len(data) == 0:
            break

        for d in data:
            prospects.append(d)

        break

    print(f"Found: {len(prospects)} Prospects")
    return prospects
