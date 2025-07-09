# Usage Instructions

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

Use the command with the `postal_code` parameter:

```bash
scrapy runspider silpo/spiders/spider.py -O output/output.json -a postal_code=03194
```

### Parameters:
- `postal_code` - postal code to determine the store location
- `-O output/output.json` - path to the file for saving results

### Examples:

```bash
# Scrape products from the store with postal code 03194
scrapy runspider silpo/spiders/spider.py -O output/185.json -a postal_code=03194

# Scrape products from another store
scrapy runspider silpo/spiders/spider.py -O output/result.json -a postal_code=01001
```

## Output

The data is saved as a JSON file in the `output/` folder and contains information about products:
- Product names
- Prices
- Categories
- Store information 