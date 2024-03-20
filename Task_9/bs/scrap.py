import requests
from bs4 import BeautifulSoup
import json
import re


def scrape_quotes(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = []
        authors = []  

        for quote_div in soup.find_all('div', class_='quote'):
            quote_text = quote_div.find('span', class_='text').get_text()
            author_name = quote_div.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]

            

            author_link = quote_div.find('a', href=True)['href']
            author_url = 'http://quotes.toscrape.com' + author_link # Corrected URL construction
            author_info = scrape_author_info(author_url)
            quote_info = {
                'quote_text': quote_text,
                'author_name': author_name,
                'tags': tags
            }
            quotes.append(quote_info)
            authors.append(author_info) 

        return quotes, authors
    else:
        print(f"Error fetching data from {url}")
        return None, None

def scrape_author_info(author_url):
    response = requests.get(author_url)
    if response.status_code == 200:
        author_soup = BeautifulSoup(response.content, 'html.parser')
        author_full_name = author_soup.find('h3', class_='author-title').get_text()
        author_born_date = author_soup.find('span', class_='author-born-date').get_text()
        author_born_location = author_soup.find('span', class_='author-born-location').get_text()
        author_description = author_soup.find('div', class_='author-description').get_text().strip()

        author_info = {
            'full_name': author_full_name,
            'born_date': author_born_date,
            'born_location': author_born_location,
            'description': author_description
        }
        return author_info
    else:
        print(f"Error fetching data from {author_url}")
        return None

if __name__ == "__main__":
    # Create a list of URLs for all pages
    urls = [f"http://quotes.toscrape.com/page/{i}/" for i in range(1, 11)]


    all_quotes = []
    all_authors = []

    # Scrape quotes from all pages
    for page_url in urls:
        page_quotes, page_authors = scrape_quotes(page_url)
        if page_quotes and page_authors:
            for quote_info in page_quotes:
                if quote_info not in all_quotes:
                    all_quotes.append(quote_info)

            for author_info in page_authors:
                if author_info not in all_authors:
                    all_authors.append(author_info)

    # Save new quotes to a JSON file
    with open('Task_9/bs/quotes.json', 'w', encoding='utf-8') as quotes_file:
        json.dump(all_quotes, quotes_file, ensure_ascii=False, indent=4)
        print("New quotes saved to quotes.json")

    # Save new authors to a separate JSON file
    with open('Task_9/authors.json', 'w', encoding='utf-8') as authors_file:
        json.dump(all_authors, authors_file, ensure_ascii=False, indent=4)
        print("New authors saved to authors.json")






