import re
from bs4 import BeautifulSoup
import requests

keywords = ["controversy", "mistreatment", "slavery", "child labor", "child labour", "abuse", "forced labor", "forced labour", "human rights", "sweatshops"]

def headline_sentences(brand_name):
    suffix = ""
    if brand_name == "Nike":
        suffix = "_(company)"
        
    if brand_name == "Walkers":
        suffix = "_(snack_foods)"

    response = requests.get(
	    url=f"https://en.wikipedia.org/wiki/{brand_name}{suffix}",
    )

    if (response.status_code != 200):
        return -1

    soup = BeautifulSoup(response.content, "html.parser")
    all_bad_sens = []
    
    for keyword in keywords:
        bad_sens = soup.find_all(text=re.compile(fr'\b{keyword}\b'))
        for sen in bad_sens:
            if 20 <= len(sen) and len(sen) <= 240:
                all_bad_sens.append(sen)
    
    return "..." + max(all_bad_sens, key = len) + "..."

def wiki_page_scrape(brand_name):
    suffix = ""
    if brand_name == "Nike":
        suffix = "_(company)"

    response = requests.get(
	    url=f"https://en.wikipedia.org/wiki/{brand_name}{suffix}",
    )

    if (response.status_code != 200):
        return -1

    keywords_occurences = {}

    soup = BeautifulSoup(response.content, "html.parser")

    for keyword in keywords:
        keywords_occurences[keyword] = soup.get_text().count(keyword)
    return keywords_occurences

#headline_nike = headline_sentences("Nike")
#print(headline_nike)

#headline_louis_vuitton = headline_sentences("Louis Vuitton")
#print(headline_louis_vuitton)

#headline_walkers = headline_sentences("Walkers")
#print(headline_walkers)
