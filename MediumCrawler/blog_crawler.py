import requests
import json
from bs4 import BeautifulSoup, CData

class blog_crawler:
    def __init__(self, blog_url):
        data = requests.get(blog_url).text
        soup = BeautifulSoup(data, "html.parser")

        # For scraping blog url and time for reading the article
        for each_meta_tag in soup.find_all("meta"):
            if each_meta_tag is not None and each_meta_tag.has_attr("property") and each_meta_tag["property"] == "og:url":
                self.url = each_meta_tag["content"]
            elif each_meta_tag is not None and each_meta_tag.has_attr("name") and each_meta_tag["name"] == "twitter:data1":
                self.article_duration = each_meta_tag["value"]
        
        # Date created, published, modified, tags & author scraped from json data
        json_data = json.loads(soup.find('script', type='application/ld+json').text)
        self.date_published = json_data["datePublished"][ : 10]
        self.date_modified = json_data["dateModified"][ : 10]
        self.author = json_data["author"]["name"]
        blog_keywords = json_data["keywords"]
        scrapped_tags = []
        for entry in blog_keywords:
            if entry.startswith("Tag:"):
                scrapped_tags.append(entry[ 4 : ])
        self.blog_tags = scrapped_tags

        # Title of article
        self.blog_title = soup.find("title").string
        