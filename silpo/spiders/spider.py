import scrapy
import json
from base64 import b64decode


def load_categories_from_file(filename):
    """Load categories configuration from JSON file"""
    with open(filename, 'r') as file:
        categories = json.load(file)
    return categories


class SilpoSpider(scrapy.Spider):
    """Spider for scraping product data from Silpo online store"""
    
    name = "silpo"
    storeId = None
    allowed_domains = ['api.catalog.ecom.silpo.ua']
    custom_settings = {
        "CONCURRENT_REQUESTS": 30,
        'RETRY_HTTP_CODES': [500, 502, 503, 520, 504, 522, 524, 408, 400, 429, 404],
        'RETRY_TIMES': 10,
        "DOWNLOAD_DELAY": 0.25,
        "AUTOTHROTTLE_ENABLED": False
    }
    
    def __init__(self, *args, **kwargs):
        super(SilpoSpider, self).__init__(*args, **kwargs)
        self.output_file = kwargs.get('output_file', 'output.json')  # Default to output.json if not provided

        # Set FEED_URI and FEED_FORMAT based on the provided output_file
        self.custom_settings = {
            'FEEDS': {
                'file://' + self.output_file: {
                    'format': 'json',
                    'overwrite': True,
                    'ensure_ascii': False,
                },
            },
        }

    def start_requests(self):    
        """Initialize requests for all categories based on store location"""
       
        # Load store locations configuration
        with open('../extra/loc.json', 'r') as f:
            locations = json.load(f)
      
        # Find store ID based on postal code
        for location in locations:
            if self.postal_code in location.get('postalCode', ''):
                self.storeId = location['filialId']
                print("store: ", self.storeId)
                break
               
        # Load categories and create requests for each category
        categories = load_categories_from_file('../extra/cat.json')
        for category in categories:
            category_id = category['categoryId']
          
            url = "https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal"
            yield self.make_request(url, self.parse_category, meta={"From": 1, "To": 33, "categoryId": category_id})
         
    def make_request(self, url, callback, **kwargs):
        """Create a Scrapy request with proper headers and data for Silpo API"""
        catId = kwargs["meta"]['categoryId']
        From = kwargs["meta"]['From']
        To = kwargs["meta"]['To']

        # Headers for Silpo API requests
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

        # Request payload for Silpo API
        data = {
            "method": "GetSimpleCatalogItems",
            "data": {
                "merchantId": 1,
                "basketGuid": "26085dd4-4a2b-4594-aaa8-6477a2c3598a",
                "deliveryType": 1,
                "filialId": self.storeId,
                "From": From,
                "businessId": 1,
                "To": To,
                "ingredients": False,
                "categoryId": catId,
                "sortBy": "popular-asc",
                "RangeFilters": {},
                "MultiFilters": {},
                "UniversalFilters": [],
                "CategoryFilter": [],
                "Promos": [],
                "deliveryDateTime": "2023-11-26T17:00:00"
            }
        }

        # Convert the Python dictionary to a JSON string
        json_data = json.dumps(data)

        # Debug logging
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Body: {json_data}")

        request = scrapy.Request(
            url=url,
            callback=callback,
            headers=headers,
            body=json_data,
            method='POST',
            meta={
                "catId": catId
            }
        )

        return request


    def parse_category(self, response):
        """Parse category response and create pagination requests for products"""
        print(json.loads(response.body))
        categoryId = response.meta.get("catId")
        
        try:
            json_response = json.loads(response.body)
            total_products = json_response['itemsCount']
            print("TOTAL", total_products)
            
            # Create pagination requests for all products in this category
            url = "https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal"
            products_per_page = 32
            total_pages = (total_products + products_per_page - 1) // products_per_page

            for page in range(total_pages):
                offset_start = page * products_per_page + 1
                offset_end = (page + 1) * products_per_page
                yield self.make_request(url, self.parse, meta={'From': offset_start, 'To': offset_end, "categoryId": categoryId})
             
        except Exception as e:
            self.logger.error(f"Error in parse_category: {e}")
         
    def parse(self, response):
        """Parse product data from API response"""
        try:
            json_response = json.loads(response.body)
            products = json_response['items']
            print(products)
            
            # Yield each product as a separate item
            for product in products:
                yield product
                
        except Exception as e:
            self.logger.error(f"Error in parse: {e}")