#!/usr/bin/env python3
"""
    Prints csv of AWS Products by screen-scraping AWS products page
"""

from requests import get
from lxml import html
import time
import json
import sys
import io

class ProductsPage:
    """
        AWS Products Page
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        # Using AWS's own API endpoint that powers their products page
        self.products_url = 'https://aws.amazon.com/api/dirs/items/search?item.directoryId=aws-products&sort_by=item.additionalFields.productCategory&sort_order=asc&size=500&item.locale=en_US'

    def products_page_content(self):
        """ http call to products url and return contents"""
        try:
            response = get(self.products_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching the page: {e}")
            return None

    def parse_products_page(self):
        """ parse products page
            return list of products
            each item is a dict """
        content = self.products_page_content()
        if not content:
            return []

        output = []
        try:
            items = content.get('items', [])
            for item in items:
                try:
                    additional_fields = item.get('item', {}).get('additionalFields', {})
                    output.append({
                        'Category': additional_fields.get('productCategory', '').strip(),
                        'Product': item.get('item', {}).get('name', '').strip(),
                        'Description': additional_fields.get('productSummary', '').strip(),
                        'Link': f"https://aws.amazon.com{item.get('item', {}).get('path', '')}"
                    })
                except Exception as e:
                    print(f"Error parsing product: {e}")
                    continue
        except Exception as e:
            print(f"Error parsing response: {e}")
            
        return output

def main():
    """ main method """
    # Set up UTF-8 output
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    products_page = ProductsPage()
    
    print("Fetching AWS products...")
    products_list = products_page.parse_products_page()
    
    if not products_list:
        print("No products found. Please check the script or try again later.")
        return

    # Print output
    quotify = lambda x: '"' + str(x).replace('"', '""') + '"'

    # Print header - keys of first item
    print(','.join(map(quotify, products_list[0].keys())))

    # Print products
    for product in products_list:
        print(','.join(map(quotify, product.values())))

if __name__ == '__main__':
    main()
