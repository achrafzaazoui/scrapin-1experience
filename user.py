import requests
from bs4 import BeautifulSoup
import csv

baseurl = 'https://ntgsjt.en.alibaba.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def scrape_page(page_number, csv_writer):
    url = f'{baseurl}productlist-{page_number}.html'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    product = soup.find('div', class_='component-product-list')
    if not product:
        return False
    
    productlist = product.find_all('div', class_='product-item')  # Adjust class name as needed
    if not productlist:
        return False

    for item in productlist:
        try:
            title = item.find('div', class_='title').get_text(strip=True) if item.find('div', class_='title') else "Title Not Available"
            link = item.find("a", class_='title-link')
            link_href = link["href"] if link and 'href' in link.attrs else "href Not Available"

            image_url = "Image URL Not Available"
            img_tags = item.find_all('img')
            for img in img_tags:
                if img.get('src'):
                    image_url = img['src']
                    break

            price = item.find('div', class_='price').get_text(strip=True) if item.find('div', class_='price') else "Price Not Available"
            freight = item.find('div', class_='freight-str').get_text(strip=True) if item.find('div', class_='freight-str') else "Shipping info not available"
            moq = item.find('div', class_='moq').get_text(strip=True) if item.find('div', class_='moq') else "MOQ Not Available"
            tags = item.find('div', class_='halfTrust-guaranteed-tags').get_text(strip=True) if item.find('div', class_='halfTrust-guaranteed-tags') else "No Tags"

            # Write to CSV
            if csv_writer:
                csv_writer.writerow([title,link_href, price, freight, moq, tags, image_url])
        except Exception as e:
            print(f"Failed to process item: {e}")

    return True

def main():
    with open('products.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Title', 'Product Image URL', 'Price', 'Freight', 'MOQ', 'Guaranteed Tags', 'Product URL'])
        page_number = 1
        while scrape_page(page_number, csv_writer):
            page_number += 1

if __name__ == "__main__":
    main()
