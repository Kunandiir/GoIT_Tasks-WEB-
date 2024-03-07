import scrapy
import json
from pathlib import Path

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    filename = "authors.json"
    with open(filename, "a", encoding="utf-8") as f:
         f.write("[\n")
    # Generate links
    def start_requests(self):
        urls = []
        for i in range(1,11):
            url = "http://quotes.toscrape.com/page/" + str(i) + "/"
            urls.append(url)
        print(urls)
        for url in urls:
        
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract quote text, author, and author link
        quotes = []

        for quote in response.css(".quote"):
            text = quote.css(".text::text").get()
            author = quote.css(".author::text").get()
            tags = quote.css(".tag::text").getall()
            author_link = quote.css(".author + a::attr(href)").get()

            # Follow the author link to get the description
            yield response.follow(author_link, self.parse_author, meta={"author": author})

            # Append quote data to the list
            quotes.append({"text": text, "author": author, "tags": tags})

        filename = "quotes.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(quotes, f, ensure_ascii=False, indent=4)

    # Parse author description
    def parse_author(self, response):
        author = response.meta["author"]
        born_date = response.css(".author-born-date::text").get()
        born_location = response.css(".author-born-location::text").get()
        description = response.css(".author-description::text").get()

        print(author)
        # Save author data to a JSON file
        filename = "authors.json"
        with open(filename, "a", encoding="utf-8") as f:
            author_data = {
                "fullname": author,
                "born_date": born_date,
                "born_location": born_location,
                "description": description.strip(),
            }
            json.dump(author_data, f, ensure_ascii=False)
            f.write(",\n")  # Add a comma and newline after each author
