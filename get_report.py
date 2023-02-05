from app import handle_request
from WebScraping.wiki_page_scrape import wiki_page_scrape

def add_score(score_map, score_name, func_name, brand_name):
    score = func_name(brand_name)
    if (score != -1): # -1 means we failed to get data from this category
        score_map[score_name] = score

def get_report(brand_name):
    score_map = {}
    
    add_score(score_map, "wiki_score", wiki_page_scrape, brand_name)
    add_score(score_map, "transparency_score", get_transparency_score, brand_name)
    add_score(score_map, "footprint_score", get_footprint_score, brand_name)
    
    return (score_map)
