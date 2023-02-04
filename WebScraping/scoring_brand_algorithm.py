from wiki_page_scrape import wiki_page_scrape
import math

def scoring_brand_algorithm(keywords_occurences):
    sumOccurences = sum(keywords_occurences.values())
    _lambda = 0.25
    return 1 - math.e ** (-_lambda * sumOccurences)

#keywords_occurences = wiki_page_scrape("Gucci")
#print(scoring_brand_algorithm(keywords_occurences))