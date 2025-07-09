import requests
import json

url = "https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal"


payload = json.dumps({
  "method": "GetSimpleCatalogItems",
  "data": {
    "merchantId": 1,
    "basketGuid": "26085dd4-4a2b-4594-aaa8-6477a2c3598a",
    "deliveryType": 1,
    "filialId": 2750,
    "From": 1,
    "businessId": 1,
    "To": 32,
    "ingredients": False,
    "categoryId": 4411,
    "sortBy": "popular-asc",
    "RangeFilters": {},
    "MultiFilters": {},
    "UniversalFilters": [],
    "CategoryFilter": [],
    "Promos": [],
    "deliveryDateTime": "2023-11-26T17:30:00"
  }
})
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'user-uid': '30b5279c-66cd-1a6e-9f03-58872e97f3b5',
  'X-SessionId': '1f5745ef95155c1d68cbcb43d0c35b77',
  'Content-Type': 'application/json',
  'Origin': 'https://shop.silpo.ua',
  'Connection': 'keep-alive',
  'Referer': 'https://shop.silpo.ua/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'TE': 'trailers',
  'Cookie': 'BIGipServer~ext-web-sites~POOL_WAF_api.catalog.ecom.silpo.ua_88=rd4o00000000000000000000ffffc0a85e66o88'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
