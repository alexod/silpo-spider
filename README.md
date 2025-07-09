# Silpo Product Scraper

A Scrapy spider for scraping product data from Silpo online store.

## Features

- Scrapes product data from Silpo API
- Supports multiple store locations based on postal codes
- Configurable categories and store selection
- Robust error handling and retry mechanisms

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alexod/silpo-spider
cd silpo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the spider with a postal code to scrape products from the corresponding store:

```bash
scrapy runspider silpo/spiders/spider.py -O output/output.json -a postal_code=03194
```

### Parameters

- `postal_code`: Postal code to determine the store location
- `-O output/output.json`: Output file path for scraped data

### Example

```bash
# Scrape products from store with postal code 03194
scrapy runspider silpo/spiders/spider.py -O output/185.json -a postal_code=03194
```

## Configuration

The spider uses configuration files in the `silpo/extrs/` directory:

- `loc.json`: Store locations and their postal codes
- `cat.json`: Product categories to scrape

## Output

The spider outputs JSON files containing product data including:
- Product names
- Prices
- Categories
- Store information

## Project Structure

```
silpo/
├── extra/
│   ├── cat.json
│   └── loc.json
├── spiders/
│   └── spider.py
├── output/
├── requirements.txt
└── README.md
```

## License

MIT License 