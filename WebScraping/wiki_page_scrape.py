import re
import math

from bs4 import BeautifulSoup

import requests
import sys

keywords = ["controversy", "mistreatment", "slavery", "child labor", "child labour", "abuse", "forced labor", "forced labour", "human rights", "sweatshops"]

def transformed_brand_name(_brand_name):
    new_name = _brand_name.lower().capitalize().replace(' ', '_').replace('&', '%26')
    print(new_name, file=sys.stdout)
    return new_name

def wiki_page_scrape(_brand_name):
    brand_name = transformed_brand_name(_brand_name)
    suffix = ""
    if brand_name == "Nike":
        suffix = "_(company)"
    if brand_name == "Walkers":
        suffix = "_(snack_foods)"

    url = f"https://en.wikipedia.org/wiki/{brand_name}{suffix}"

    response = requests.get(url)

    if (response.status_code != 200): # Didn't find wiki link of brand name
        print(f"Couldn't find wiki link of brand name: {url}", file=sys.stdout)
        return None

    keywords_occurences = {}

    soup = BeautifulSoup(response.content, "html.parser")

    for keyword in keywords:
        keywords_occurences[keyword] = soup.get_text().count(keyword)
    if sum(keywords_occurences.values()) == 0:
        return None
    else:
        return scoring_brand_algorithm(keywords_occurences)

#headline_nike = headline_sentences("Nike")
#print(headline_nike)

#headline_louis_vuitton = headline_sentences("Louis Vuitton")
#print(headline_louis_vuitton)

#headline_walkers = headline_sentences("Walkers")
#print(headline_walkers)

def scoring_brand_algorithm(keywords_occurences):
    sumOccurences = sum(keywords_occurences.values())
    _lambda = 1
    return _lambda * math.e ** (-_lambda * sumOccurences)
