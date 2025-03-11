import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import time
from urllib.parse import urljoin
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KLRacingScraper:
    def __init__(self, base_url: str = "https://shop.klracing.se", delay: float = 1.0):
        """
        Initialize the scraper with base URL and delay between requests
        
        Args:
            base_url (str): The base URL of the website
            delay (float): Delay between requests in seconds
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_urls_from_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Extract all URLs from the sitemap
        
        Args:
            sitemap_url (str): URL of the sitemap
            
        Returns:
            List[str]: List of product URLs
        """
        try:
            response = self.session.get(sitemap_url)
            response.raise_for_status()
            
            # Parse the XML content
            root = ET.fromstring(response.content)
            
            # Define the namespace
            ns = {'sm': 'http://www.google.com/schemas/sitemap/0.84'}
            
            # Find all URL elements using the correct namespace
            urls = []
            for url in root.findall('.//sm:loc', namespaces=ns):
                if url.text:
                    urls.append(url.text)
            # Add debugging output
   
            # Filter only product URLs
            product_urls = [url for url in urls if '/artiklar/' in url]

            # product_urls = [url for url in urls if '/artiklar/' in url and url.endswith('.html') and not url.endswith('index.html')]
            
            
            logger.info(f"Found {len(product_urls)} product URLs in sitemap")
            return product_urls
            
        except Exception as e:
            logger.error(f"Error parsing sitemap: {e}")
            return []

    def scrape_product(self, url: str) -> Optional[Dict]:
        """
        Scrape product information from a product page
        
        Args:
            url (str): URL of the product page
            
        Returns:
            Optional[Dict]: Dictionary containing product information or None if failed
        """
        try:
            time.sleep(self.delay)  # Respect the website by adding delay
            response = self.session.get(url)
            response.raise_for_status()
            
            # Use html5lib parser instead of lxml
            soup = BeautifulSoup(response.content, 'html5lib')
            
            # Initialize product data dictionary
            product_data = {
                'url': url,
                'name': None,
                'price': None,
                'description': None,
                'specifications': {},
                'images': [],
                'category': None,
                'sku': None
            }
            breakpoint() 
            # Extract product name
            product_name = None
            name_elem = soup.find('h1', class_='product-title')
            xpath_elem = soup.find('a', {'href': '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div[6]/form/div/table/tbody/tr/td[2]/a/font/font'})
            if xpath_elem:
                product_name = name_elem
                breakpoint()
            if product_name:
                product_data['name'] = product_name.text.strip()
            
            # Extract price
            price_elem = soup.find('span', class_='price')
            if price_elem:
                product_data['price'] = price_elem.text.strip()
            
            # Extract description
            desc_elem = soup.find('div', class_='product-description')
            if desc_elem:
                product_data['description'] = desc_elem.text.strip()
            
            # Extract images
            image_elements = soup.find_all('img', class_='product-image')
            product_data['images'] = [
                urljoin(self.base_url, img.get('src'))
                for img in image_elements
                if img.get('src')
            ]
            
            # Extract category breadcrumb
            breadcrumb = soup.find('div', class_='breadcrumb')
            if breadcrumb:
                categories = [item.text.strip() for item in breadcrumb.find_all('a')]
                product_data['category'] = ' > '.join(categories)
            
            # Extract SKU/Article number if available
            sku_elem = soup.find('span', class_='article-number')
            if sku_elem:
                product_data['sku'] = sku_elem.text.strip()
            
            logger.info(f"Successfully scraped product: {product_data['name']}")
            return product_data
            
        except Exception as e:
            logger.error(f"Error scraping product {url}: {e}")
            return None

    def save_to_json(self, products: List[Dict], filename: str = 'products.json'):
        """
        Save scraped products to a JSON file
        
        Args:
            products (List[Dict]): List of product dictionaries
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully saved {len(products)} products to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")

    def run(self, sitemap_url: str):
        """
        Run the complete scraping process
        
        Args:
            sitemap_url (str): URL of the sitemap
        """
        # Get all product URLs from sitemap
        product_urls = self.get_urls_from_sitemap(sitemap_url)
        breakpoint()
        # Scrape each product
        products = []
        # for url in product_urls:
        #     product_data = self.scrape_product(url)
        #     if product_data:
        #         products.append(product_data)
        for url in product_urls[:10]:
            product_data = self.scrape_product(url)
            if product_data:
                products.append(product_data)
        
        # Save results
        self.save_to_json(products)

if __name__ == "__main__":
    # Initialize scraper
    scraper = KLRacingScraper()
    
    # Run the scraper
    scraper.run("https://shop.klracing.se/sitemap.xml") 