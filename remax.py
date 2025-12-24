from prospects import Prospect

import requests
import json
from bs4 import BeautifulSoup

def extract_data_from_html(html, streetsFilter, citiesFilter):
    soup = BeautifulSoup(html, "html.parser")

    results = []

    scripts = soup.find_all("script", type="application/json")

    for script in scripts:
        if not script.string:
            continue

        try:
            data = json.loads(script.string)
            listings = data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['results']
            for lst in listings:
                addr = lst['address']
                lower_addr = addr.lower()
                
                city = lst['mlsCity']
                lower_city = city.lower()
                
                ignore = False

                for str in streetsFilter:
                    if str.lower() in lower_addr:
                        ignore = True

                for ct in citiesFilter:
                    if ct.lower() == lower_city:
                        ignore = True

                if int(lst['baths']) == 0:
                    ignore = True

                if int(lst['beds']) == 0:
                    ignore = True

                if not ignore:
                    results.append(Prospect(
                        price=lst['listPrice'], 
                        addr=lst['address'], 
                        beds=lst['beds'], 
                        baths=lst['baths'], 
                        town=lst['mlsCity'], 
                        url='www.remax.ca/' + lst['detailUrl'], 
                        postingDate=lst['listingDate'],
                        listingId=lst['listingId'],
                        lat=lst['lat'],
                        long=lst['lng'],
                        liked=0
                    ))
        except json.JSONDecodeError:
            continue

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
        "gad_source": config_data.gad_source,
        "gad_campaignid": config_data.gad_campaignid,
        "gbraid": config_data.gbraid,
        "gclid": config_data.gclid,
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

        data = extract_data_from_html(response.text, config_data.streetsToAvoid, config_data.citiesToAvoid)
        if len(data) == 0:
            break

        for d in data:
            prospects.append(d)

    return prospects
