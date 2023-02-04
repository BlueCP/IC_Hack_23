import re
from bs4 import BeautifulSoup
import requests

keywords = ["mistreatment", "slavery", "child labor", "child labour", "abuse", "forced labor", "forced labour", "human rights", "sweatshops"]

def wiki_page_scrape(brand_name):
    suffix = ""
    if brand_name == "Nike":
        suffix = "_(company)"

    response = requests.get(
	    url=f"https://en.wikipedia.org/wiki/{brand_name}{suffix}",
    )

    if (response.status_code != 200):
        print("Brand Name: ", brand_name)
        print("Something wrong, response status code is: ", response.status_code)

    keywords_occurences = {}

    soup = BeautifulSoup(response.content, "html.parser")
    for keyword in keywords:
        keywords_occurences[keyword] = soup.get_text().count(keyword)
    return keywords_occurences

#keywords_occurences = wiki_page_scrape("Louis_Vuitton")
#print(keywords_occurences)